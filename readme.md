# Amazon Bunny Tools

My current company is doing a lot of stuff with AWS so here is where I keep my stubs and scripts


## findLocalDomains.py
So I was tasked with auditing all 580 domains we have in Route53. This quick app;
* pulls all of the domains
* sorts out the A and CNAMES
* queries the recods for return code and final url (to hightlight redirects and parked domains)
* outputs cvs

It's not as resuable as most of my things but should be reusable in a few contexts with hacking
