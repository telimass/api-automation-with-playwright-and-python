### QUESTION 1:
You have created a transaction on the chain, and been requested to prove it's yours. You can’t access your private key. How else can you prove the transaction is yours?

* If the transaction includes metadata or additional information that only you would know, you can use this as evidence of your involvement;
* It may be possible to prove a transaction without revealing any single private key by showing that multiple authorized parties have signed off on it;
* Zero-Knowledge Proof;
* Using a custodial wallet service, you can request the service to create and sign a transaction on your behalf with pre-agreed parameters, such as the
recipient address and amount. You can then provide the signed transaction to the recipient as proof of your initiation, even without access to your private
key. This method allows you to prove transaction initiation without revealing your private key, as the transaction signing is done by the custodial service on
your behalf.


### QUESTION 2:
You have sent X amount of assets from wallet A to Wallet B. How would you verify the transaction is finalized (provide detailed steps)?

* Need to double-check transactions status (if it really appeared there). For example here: etherscan;
* Check wallet's balance before and after transaction;
* Confirm that the wallet B is correct and corresponds to the intended recipient to ensure that the funds are sent to the correct destination;
* Check transaction's confirmations number, since more confirmations guarantee a more secure transaction which are less likely to be reversed.


### QUESTION 3:
You have sent X amount of your XRP from wallet A to wallet B. On your side transaction is completed. The Wallet B still did not receive funds. What can be wrong? Detail your thoughts.

* Usually it's because of overloaded network (high traffic which causes delays);
* Destination address was wrong (non-existing address, or you've sent token to wrong address);
* Maybe it's still in pending status? Also need to wait;
* Is wallet B fully synced in XRP network? It needs time before displaying incoming transactions;
* Wallet B can have some technical issues on software or infra level;
* Might be problem with XRP destination tag which was not included into transaction.


### QUESTION 4:
You have 3 ETH in wallet A. You withdraw 3 ETH from wallet A to wallet B. Transaction failed. Explain why?

* Wallet A may not have had enough ETH to cover the transaction amount + gas fees, resulting in a failed transaction;
* Gas limit (set for transaction) is too low. Need to increase it;
* Problems with network because of overloading.