# BitCatalyst
### Video Demo:
### Brief description:

BitCatalyst is a simulated off-chain trading environment where users are able to perform paper trades on a select few cryptocurrencies.

The platform is designed with beginners in mind, providing them with a bespoke and risk-free setting to pioneer and refine their strategies and techniques. The website consists of twelve pages, including the error page.  It also features a polished and engaging Bootstrap grid layout, ensuring that the page is organised and easy to navigate. A dark color scheme was also chosen for better visibility in a dimly-lit environment, while also causing less strain for users.

### What makes BitCatalyst special?

To most people, trading seems like a complex and cumbersome process; the endless charts and jargons can be overwhelming. Most established services also make it challenging for users to try their hand at basic trades before depositing any real money.

Then we have **BitCatalyst**! A one-stop solution for inexperienced traders to test the waters and build up their confidence gradually. BitCatalyst has a simple user-interface, making it accesible and easy to navigate, while requiring no deposit of any sort.

**Here are some features that users can look forward to:**

- Creating an account requires minimal personal information, with your name and email address being the only mandatory private details. Users are also made to set a seed phrase for enhanced security, which also prepares them for when they eventually open an on-chain wallet.

- Once registered, users can head over to the **/trade** page to select from a curated list of cryptocurrencies that are of high market-cap, and open a 'long' or 'short' position with just a few clicks. Each user is credited with $5000 of simulated currency, but are able to 'deposit' or withdraw' as much as they would like in the **/profile** page.

- A obtained from a TradingView API is also available in both the **/index** and /trade pages for users to make a more informed decision.

- The /index page would display a table of all the trades that are open, with live PnL (Profit & Loss).
    > [!NOTE]
    > You are allowed to hedge by opening a short and long position for any coin at the same time.

- Then comes the **/analyse** page. Once you have closed your positions, they would appear here. A detailed breakdown of each of your trade, your average PnL and Win Rate, and other metrics such as your top coins are available here for your perusal! Basic, but effective for those starting off.

- Last but not least, we have the **flagship** feature of the platform, which is non other than the **/journal** page! Users are able to write a **short summary** of how their trading day transpired here, which they are able to refer to in the future where neccesary. It is common for people to land in the same pitfalls repeatedly, especially in the initial stages where many **impulsive decisions** are made. With this feature, however, users are are able to revisit some of the **past mistakes or lessons** they learnt-it could even be favourable strategies-before they open a position, keeping them **grounded and focused**. Over time, they would hone their **trading instincts** and see vast improvements.

### Running the program:

BitCatalyst is a webapp built with Flask, Javascript and HTML. Owing to it submission as a CS50 final project, it also relies on methods and functions imported from CS50's personal library.

Therefore, it is important to note that the webapp locally can only run when the cs50 library is installed. _Refer to requirements.txt for all the dependencies_.

**For those running the code using Github**:

1. To run the code, head over to [Github codepsaces](https://cs50.dev/).

2. Log in to your dedicated codespace with your github account.

3. Once in session, enter:
    ```
    wget -----
    unzip ---.zip
    cd YOUR_FOLDER
    flask run
    ```
4. You should see a pop-up notifying that the webapp is running on a specific port. Click on the link, and you are good to go!

5. This project is open-source, so please feel free to clone and modify the code as you wish.


**For those running the program locally**:

1. Ensure that you have installed python.

2. Type the following in the terminal of your IDE:
    ```
    wget -----
    unzip ---.zip
    cd YOUR_FOLDER
    pip install flask cs50
    flask run

   ```
3. Assuming you have connected to a serviceable port, the webapp should now be accessible through the link tied to the port,

4. There you have it! You may now proceed to explore BitCatalyst.

### Future plans and miscellaneous information:

**Some pages that are in the webapp but not highlighted**:

- The **/landing** page where users are greeted when they launch the webapp. It contains two columns, one containing a large-font phrase to grab the attention of visitors, and a supporting image on the right. They form the 'hero' component of the page as is styled using CSS. A short description of the website is also available in a row below.

- The **/register**, **/login**, **/reset** and **/postreset** pages are simple and functional, allowing users to create accounts and assist them with changing their password should they forget. The form takes up the entire page.

- Every page also includes a **footer** with company details, although they are largely irrelevant and just for banter.

**Hopes for the future**

- Definitely hoping to continue developing this as a personal project outside of CS50's environment, when time permits. I have been working on an algorithm for real-time market intelligence and an enhanced trade analysis protocol separately, that I hope to integrate with this program some time in the near future.

- I would also like to attempt this project again with React, Tailwindcss and Supabase to provide a more interactive and up-to-date user experience.


**END**
