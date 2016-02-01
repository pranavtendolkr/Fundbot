a='''"Value Research Online"
"Date: 29-Jan-2016 15:19"
"Company","Sector","Industry","Price","PriceDate","1-Day Chg. (%)","52-Week High","52-Week Low","P/E","P/B","Enterprise Value (Cr)","Market Cap (Cr)"
"A.F. Enterprises Ltd.","Financial","Invest.Services","46.95","Jan 29, 14:49","-1.98","648","47.9","507.57","6.54","18.56","18.78"
'''

print ''.join(a.split('\n')[2:])
import string
for letter in string.uppercase + '2378':
    print letter
