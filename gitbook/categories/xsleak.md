# Cross-site Leak (XSLeak)

Cross-site leaks (aka XS-Leaks, XSLeaks) are a class of vulnerabilities derived from side-channels 1 built into the web platform. They take advantage of the web’s core principle of composability, which allows websites to interact with each other, and abuse legitimate mechanisms 2 to infer information about the user. One way of looking at XS-Leaks is to highlight their similarity with cross-site request forgery (CSRF 3) techniques, with the main difference being that instead of allowing other websites to perform actions on behalf of a user, XS-Leaks can be used to infer information about a user.

## Resources

* [XS-Leaks wiki](https://xsleaks.dev/)

## Challenges

* [Leakynote (corCTF 2023)](/gitbook/challenges/corCTF-2023/leakynote.md)
* [Leakless Note (SekaiCTF 2023)](/gitbook/challenges/../gitbook/challenges/sekaictf2023/leakless-note.md)