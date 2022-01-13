# algo-burner
Burner address for Algorand's blockchain

Apparently it was a problem that people couldn't verifiably burn ASAs, and the current best way I've seen was sending the ASA to an account that you create and opt in and then rekey that account to a verifiably unknown account. I thought that was clunky so I made another way.

Send an application call to the smart contract at appID 541574524 with the asset you want it to opt into being the firt entry in the assets array. Then send the ASAs you want to burn to the application address at AEI5EMQIYQTRTDV4BCZSVNQKO3LYOBKJAL67YY4OO5WJGC443NOYDDPC2Y

I used the compiled version of the exact file in this repo for everything, if you'd like to verify. You're also welcome to create this application yourself and just do that