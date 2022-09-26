# dca

dollar-cost averaging dla s&p 500 na platformie xtb

1. znaleźć dokumentację dla API XTB
2. założyć konto na sandboxie XTB
3. odpalić jakiegoś requesta w jupyter notebook
4. tworzenie zlecenia przez API
5. przygotować dane zlecenia które ma się tworzyć
6. napisać skrypt korzystający z apscheduler który kupuje co minutę jednostkę CSPX S&P500

```
gcloud pubsub topics create buy_on_xtb
```

```
gcloud functions deploy dca-xtb-function \
--gen2 \
--region=europe-central2 \
--runtime=python310 \
--source=. \
--entry-point=kupuj \
--trigger-topic=buy_on_xtb \
--env-vars-file=.env.yaml
```

```
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

```
gcloud scheduler jobs update pubsub buy_usa_bonds_daily \
    --location=europe-central2 \
    --schedule="0 14 * * 1-5" \
    --topic=buy_on_xtb \
    --message-body='{"symbol": "IBTA.UK", "volume": 6}'
```

```
# co tydzień we wtorek do 21 dnia miesiąca - czyli co tydzień trzy razy w miesiącu
gcloud scheduler jobs update pubsub buy_snp500_three_times_a_month \
    --location=europe-central2 \
    --schedule="30 14 1-21 * 2" \
    --topic=buy_on_xtb \
    --message-body='{"symbol": "CSPX.UK_9", "volume": 1}'
```

```
gcloud pubsub topics publish buy_on_xtb --message='{"symbol": "IBTA.UK", "volume": 6}'
```
