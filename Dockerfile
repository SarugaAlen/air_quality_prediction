FROM mambaorg/micromamba:latest AS builder

WORKDIR /app

COPY environment.yml /tmp/environment.yml
RUN micromamba create -n py310 --file /tmp/environment.yml && \
    micromamba clean --all --yes

FROM mambaorg/micromamba:latest

WORKDIR /app

COPY --from=builder /opt/conda/envs/py310 /opt/conda/envs/py310
ENV PATH="/opt/conda/envs/py310/bin:$PATH"

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
