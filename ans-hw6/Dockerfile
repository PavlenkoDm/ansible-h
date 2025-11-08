FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openssh-client \
    sshpass \
    git \
    tree \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir ansible

WORKDIR /ansible

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

CMD ["tail", "-f", "/dev/null"]