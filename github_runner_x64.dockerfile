FROM ubuntu:18.04

ENV RUNNER_VERSION=2.273.5
ENV DOCKERVERSION=18.06.3-ce

RUN useradd -m actions
RUN apt-get -yqq update && apt-get install -yqq curl jq wget

# Retrieve GitHub Runner
RUN \
  LABEL="$(curl -s -X GET 'https://api.github.com/repos/actions/runner/releases/latest' | jq -r '.tag_name')" \
  RUNNER_VERSION="$(echo ${latest_version_label:1})" \
  cd /home/actions && mkdir actions-runner && cd actions-runner \
    && wget https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz \
    && tar xzf ./actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz

# Retrive and install only Docker's CLI
# Credits: Aaron V via https://stackoverflow.com/questions/38675925/is-it-possible-to-install-only-the-docker-cli-and-not-the-daemon
RUN curl -fsSLO https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKERVERSION}.tgz \
  && tar xzvf docker-${DOCKERVERSION}.tgz --strip 1 \
                 -C /usr/local/bin docker/docker \
  && rm docker-${DOCKERVERSION}.tgz

# Add the actions user to the docker group so docker commands could be run withou sudo
RUN groupadd docker
RUN usermod -aG docker actions

# Setting up entry point
WORKDIR /home/actions/actions-runner
RUN chown -R actions ~actions && /home/actions/actions-runner/bin/installdependencies.sh

COPY github_runner.entry_point.sh .
RUN chmod 555 github_runner.entry_point.sh

USER actions
# CMD ["/bin/sh"]
CMD exec ./github_runner.entry_point.sh