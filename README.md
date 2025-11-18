# en1gma-v2-account-spammer

This spammer was originally made back when the semi-famous william1337 launched a website for his cheat en1gma v2. Using this script, around 600,000 accounts were registered — all from just three PCs.

Back then it was a simple async script. Now I’ve upgraded it with threading and proper database storage instead of dumping everything into a .txt.

The website is dead now anyway, so I decided to leak this crap.

This whole situation is a good reminder: if you’re building your own project, think about protection. There was no rate-limit bypass, no block against mass registrations, and not even email validation (like checking if the email actually exists). Because of that, it was possible to pump out hundreds of thousands of accounts without losing anything.

After about 3 hours of non-stop registrations, the site just went down. It tried to recover a few times, but eventually completely died.