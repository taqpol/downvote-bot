# downvote-bot

A simple exercise in automating browser actions. Staggers downvote actions by 90-120s intervals to attempt to avoid reddit's downvote spree detection mechanisms. Doesn't downvote comments older than 2 days. Reads from a text file to allow you to downvote multiple users at once. Using the API would have been too obvious; using Selenium should make actions appear to be initiated by a user. User agent has been changed to something less conspicuous, though I don't know if anything else is being transmitted that would lead to detection.

NOTE: This script takes a very long time to run. The pauses in between each downvote are necessary.

Requires chromedriver for Windows in the working directory.

No guarantees that it will actually impact your targets' comment karma. It only downvotes.

Add a text file to the working directory with return-separated names, and specify that file when prompted to.

Throws an error about being unable to write to Document, but doesn't appear to affect functionality.
