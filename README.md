# downvote-bot

A simple exercise in automating browser actions. Staggers downvote actions by 90-120s intervals to attempt to avoid reddit's downvote spree detection mechanisms. Doesn't downvote comments older than 2 days. Reads from a text file to allow you to downvote multiple users at once. Using the API would have been too obvious; using Selenium should make actions appear to be initiated by a user. 

Requires chromedriver for Windows in the working directory.

No guarantees that it will actually impact your targets' comment karma. It only downvotes.

Add a text file to the working directory with return-separated names, and specify that file when prompted to.

Throws an error about being unable to write to Document, but doesn't appear to affect functionality.
