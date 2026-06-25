# How to run this on your terminal

## 1. Get your Yoco TEST secret key
- Log into the Yoco account on your laptop
- Go to: Settings (or "Online Payments") > Checkout API / API Keys
- Copy the key that starts with `sk_test_...` (NOT the live one yet — test first)

## 2. Install dependencies
Open your terminal in this folder and run:

    pip install -r requirements.txt

## 3. Set your secret key
Still in the terminal, run (replace with your real test key):

    export YOCO_SECRET_KEY="sk_test_xxxxxxxxxxxxxxxxxxxx"

(On Windows, use `set YOCO_SECRET_KEY=sk_test_xxxx` instead)

## 4. Run the site

    python app.py

## 5. Open it
Go to: http://localhost:5000

Enter an amount and click Pay. You'll get redirected to Yoco's real test checkout page.
Use Yoco's official test card numbers (search "Yoco test card numbers" in their docs)
to simulate a successful payment without spending real money.

After a successful test payment, you'll land back on the Thanks page with the heart.

---

## Adding the real photo
1. Drop the approved image file into the `static` folder, e.g. `static/photo.jpg`
2. In `templates/index.html`, replace this block:

    <div class="image-wrap">
      Image goes here...
    </div>

   with:

    <img src="/static/photo.jpg" alt="" style="width:100%; aspect-ratio:1/1; object-fit:cover; display:block;" />

## Going live later
- Swap the test key for the live key (`sk_live_...`) once you deploy for real
- Update BASE_URL to your real domain (set via the BASE_URL environment variable)
- Deploy to something like Render or Railway so the link works for everyone, not just your laptop
- For real production use, add webhook verification (Yoco recommends not trusting
  successUrl alone) — happy to help with that step when you're ready to deploy
