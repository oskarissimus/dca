# dca

dollar-cost averaging dla s&p 500 na platformie xtb

1. znaleźć dokumentację dla API XTB
2. założyć konto na sandboxie XTB
3. odpalić jakiegoś requesta w jupyter notebook
4. tworzenie zlecenia przez API
5. przygotować dane zlecenia które ma się tworzyć
6. napisać skrypt korzystający z apscheduler który kupuje co minutę jednostkę CSPX S&P500

```
gcloud pubsub topics create buy_usa_bonds
```

```
gcloud functions deploy dca-xtb-function \
--gen2 \
--region=europe-central2 \
--runtime=python310 \
--source=. \
--entry-point=kupuj \
--trigger-topic=buy_usa_bonds \
--env-vars-file=.env.yaml
```

```
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

```
gcloud scheduler jobs create pubsub buy_usa_bonds_daily \
    --location=europe-central2 \
    --schedule="0 14 * * 1-5" \
    --topic=buy_usa_bonds \
    --message-body="dupa"
```

```
gcloud pubsub topics publish buy_usa_bonds --message="dupa"
```
