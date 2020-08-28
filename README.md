# keep-tdt-id-bot  
The bot allows you to get unspent tdt_id by lot size to return your BTC to dApp TBTC Keep Network. 
This is the simplest way to demonstrate how the main method `GET /api/op/tdt_id?lot={amount}&token={token}` of Keep Indexer (https://github.com/fedorov-m/KeepIndexer) works.

## Requirements  
- python v3.6+
- own TG bot token (you can get it here - @BotFather)

## Install  
`pip3 install -r requirements.txt`  
Enter your bot_token and url of keep-indexer API in the configuration file

## How it works
You choose the size of the lot and get a random unspent TDT_ID  
![alt text](https://miro.medium.com/max/692/1*OH8V1bIImki-heR38zubtg.png)  
