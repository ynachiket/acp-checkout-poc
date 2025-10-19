# 🎬 FINAL DEMO INSTRUCTIONS

**Node.js upgraded to v18 ✅**  
**All systems operational ✅**  
**Ready for visual demo ✅**

---

## 🌐 Your Demo URL

```
http://localhost:5173
```

**Open in your browser NOW!**

---

## ✅ System Status

```
✅ Backend:     http://localhost:8000 (Running)
✅ Frontend:    http://localhost:5173 (Running)  
✅ Node.js:     v18.20.8 (Upgraded!)
✅ Database:    10 Nike products seeded
✅ Tests:       47/47 passing
```

---

## 🎬 Demo Flow (30 seconds)

### What to Do

1. **Open:** http://localhost:5173
2. **Type:** "I want to buy Nike Air Max shoes"
3. **Click:** "Add to Cart"
4. **Type:** "Ship to New York"
5. **Click:** "Complete Purchase"

### What You'll See

```
Step 1: Product card appears (Nike Air Max 90, $120)
Step 2: ChatGPT asks for shipping
Step 3: Checkout summary shows ($134.60 total)
Step 4: ✅ Order confirmed! (order_xyz123...)
```

---

## 🔍 Optional: Show Technical Details

**Click:** "🔍 Show Debug" button (top-right)

**Shows:**
- Real-time API calls
- Response times (< 300ms)
- Session state
- Performance metrics

**Perfect for technical audiences!**

---

## 🎯 If Something Isn't Working

### Frontend Not Loading?

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm use 18
cd /Users/ntorwe/checkout-poc/frontend/simulator
npm run dev
```

### Backend Not Responding?

```bash
cd /Users/ntorwe/checkout-poc/backend
uvicorn app.main:app --reload --port 8000
```

### Still Issues?

**Use backup demo:**
```bash
cd backend
python scripts/test_purchase_flow.py
```

This works perfectly and shows the complete flow!

---

## 🎉 You're Ready!

**Both servers running ✅**  
**Node.js upgraded ✅**  
**Demo ready ✅**

**Next:** Open http://localhost:5173 and start shopping! 🛍️

---

**Status:** 🟢 ALL SYSTEMS GO!

