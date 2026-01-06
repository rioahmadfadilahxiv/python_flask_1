from flask import Flask, render_template, request
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json

# === KONFIGURASI ===
# Cookie dalam format JSON (disalin dari EditThisCookie atau sejenisnya)
BING_COOKIES_JSON = '''
[{"domain":".bing.com","expirationDate":1783183516.435487,"hostOnly":false,"httpOnly":false,"name":"MUID","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"0FC5DE4431D765471DD1C8CB305064B9"},{"domain":".bing.com","expirationDate":1776869721.113181,"hostOnly":false,"httpOnly":true,"name":"_EDGE_V","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"1"},{"domain":".bing.com","expirationDate":1776869721.113316,"hostOnly":false,"httpOnly":false,"name":"SRCHD","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"AF=NOFORM"},{"domain":".bing.com","expirationDate":1776869721.113457,"hostOnly":false,"httpOnly":false,"name":"SRCHUID","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"V=2&GUID=7AEBD7BF75314FB3B3000E714D4EAEB4&dmnchg=1"},{"domain":".bing.com","expirationDate":1780742507.511612,"hostOnly":false,"httpOnly":false,"name":"_UR","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"QS=0&TQS=0&Pn=0"},{"domain":".bing.com","expirationDate":1780742507.513211,"hostOnly":false,"httpOnly":false,"name":"BFBUSR","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"BFBHP=0"},{"domain":".bing.com","expirationDate":1783183532.429672,"hostOnly":false,"httpOnly":true,"name":"MUIDB","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"0FC5DE4431D765471DD1C8CB305064B9"},{"domain":"rewards.bing.com","expirationDate":1783185380.573672,"hostOnly":true,"httpOnly":true,"name":"vdp","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"0"},{"domain":".bing.com","expirationDate":1780471101.163607,"hostOnly":false,"httpOnly":false,"name":"ANON","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"A=56DAC3C2DCF3A0353102AA09FFFFFFFF"},{"domain":".bing.com","expirationDate":1780202539.147304,"hostOnly":false,"httpOnly":false,"name":"_tarLang","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"default=id"},{"domain":".bing.com","expirationDate":1780202539.151919,"hostOnly":false,"httpOnly":false,"name":"_TTSS_IN","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"hist=WyJlbiIsImF1dG8tZGV0ZWN0Il0=&isADRU=0"},{"domain":".bing.com","expirationDate":1780202539.153391,"hostOnly":false,"httpOnly":false,"name":"_TTSS_OUT","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"hist=WyJpZCJd"},{"domain":".bing.com","expirationDate":1780202475.227923,"hostOnly":false,"httpOnly":false,"name":"SRCHUSR","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"DOB=20251024&DS=1&POEX=W"},{"domain":".bing.com","expirationDate":1780299086.205873,"hostOnly":false,"httpOnly":false,"name":"_BINGNEWS","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"SW=1905&SH=963"},{"domain":".bing.com","expirationDate":1780742508.569362,"hostOnly":false,"httpOnly":false,"name":"_HPVN","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"CS=eyJQbiI6eyJDbiI6MTcsIlN0IjowLCJRcyI6MCwiUHJvZCI6IlAifSwiU2MiOnsiQ24iOjE3LCJTdCI6MCwiUXMiOjAsIlByb2QiOiJIIn0sIlF6Ijp7IkNuIjoxNywiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyNS0xMi0wOFQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIlRucyI6MCwiRGZ0IjpudWxsLCJNdnMiOjAsIkZsdCI6MCwiSW1wIjoxNDMxLCJUb2JuIjowfQ=="},{"domain":".bing.com","expirationDate":1780916138.512776,"hostOnly":false,"httpOnly":true,"name":"USRLOC","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"HS=1&ELOC=LAT=-7.651411533355713|LON=112.90544128417969|N=Panggungrejo%2C%20Jawa%20Timur|ELT=10|"},{"domain":".bing.com","expirationDate":1780939635.327296,"hostOnly":false,"httpOnly":false,"name":"_RwBf","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"r=0&ilt=15&ihpd=0&ispd=3&rc=3202&rb=3202&rg=6750&pc=3202&mtu=0&rbb=0&clo=0&v=3&l=2025-12-10T08:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&ard=0001-01-01T00:00:00.0000000&rwdbt=1765230973&rwflt=1765161761&rwaul2=0&g=&o=16&p=search_and_earn&c=ML2W7B&t=8115&s=2025-07-21T13:55:28.6345646+00:00&ts=2025-12-10T17:27:15.3674866+00:00&rwred=0&wls=2&wlb=0&wle=0&ccp=2&cpt=0&lka=0&lkt=0&aad=0&TH=&cid=0&gb=2025w30_c&mta=0&e=haZhADZ4bBsbzF7q-iOBYYm-yiDetSvjRS4iU8EnXlCJ5Midxm_rWDRUiVbSMW4cyHkujw--ZtJGHde0Ipp_j1Xwytmpw5pm22xcQJ2nvdQ&A="},{"domain":".bing.com","expirationDate":1780944176.539831,"hostOnly":false,"httpOnly":false,"name":"SRCHHPGUSR","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"PREFCOL=1&BRW=XW&BRH=M&CW=1738&CH=873&SCW=1725&SCH=1852&DPR=1.1&UTC=420&PRVCW=1738&PRVCH=873&SRCHLANG=id&PV=19.0.0&B=0&IG=952626841466434D95FBB5CBDCC14C5B&EXLTT=31&HV=1765190576&HVE=CfDJ8BJecyNyfxpMtsfDoM3OqQv3kUQxDEsJIRuPFafV7evThhRBXPULIECQuv0Ctq4xJcFa3efIjZOHQ8bSQIPrLzDURHRxJWnWgUUHsfjuq3IkWheDL_Mco4I85nTBmslrIwVQvw0Cn3SwxtCws99VNzIFU1-euBB9f9NYyGRUZOhViKRV44V6biHbvCblXRZVUQ"},{"domain":".bing.com","expirationDate":1767717904,"hostOnly":false,"httpOnly":false,"name":"MSCC","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"NR"},{"domain":"rewards.bing.com","expirationDate":1768841133.429536,"hostOnly":true,"httpOnly":true,"name":"tifacfaatcs","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"CfDJ8LfTkwiAHdVDsG3ePT4u9-p6ZwOAQmIjCOIxtEponA2QkDpZ8lbe8UJbATmwxa6ZKokTmQLkknsRB4XCYc7OkPn8mPOKJf_33YZzwfcUlkNNi5A1CX8ku8KgZrPmi-68ReWcQ-a0A3t7wKYSE2H3aHOiUih1JGt6JNFV8sOcQk2fNpnbDAajKHQRAlpLSFXx2JcShJGE3zmt7B-jUYS4MecJuW1yFm9yRz-cnnwLRYBvpEsiunozRyTpGlfIKrxdw8gKQVdWCpyWHqRZRd2-R962HWfx3rr_L775-uSUlzwPSNGRvdrqxQXqxBU5aeNjbsGxlE_g3TVEoG-NKn3HQa_kvA7bDcV8d6AVMuwupXyKmatasm4HvbzdyRH54on5dbZMyv-YOfaTnIXDoQiTvThAvk3j-QkhDFlCPYRRvGnoRdfxT538zJieU-X9yJHMLPXoP5WKcsMO8F4m656Ykv-akJM2VDgUF8sc6B9Hw60l94dRY-B9PEZ1MTnZ8pQB312QxDndh4hXBG6dk81ztijUWZja1QHdPLWGTc3gQA2hRlAH1sjRQ0fL5azEFaD0VkHYoruKGMBIcTQg9Nw2AXZU7VOHI-gS4srkpVnFPOuRyxKNnSOr9reM3AmiTfUSnYyas4MVLQLC7KcDcaPu6JIxVkC24QXzGAjhBCFfMwTR687hwOl39B7Iy9u4cKZ_nxuPj6gjUZkk2ro6G7n7A_Nlto00isHVg7t4a2vR-CE0UhcHiE91IoAm_JiH3RwuReaB-xV_wWGG-GgNDQTiAdSw45TU3CrQaUQu5KJzpm2VBoR0OgJdPo8WELi1mRM29GR2JI7O4OHOOQtjbseXV3eROXGuwXwjRRJPoRcFjt1XmKLDRr_p0WzZbN3KhxeOaUbM_QXyRIeGro3aGoythGveLob_887_csmqFsb4b_vNAsKj44JeDtKY7HlhJTA53Mm7frszS1l4Qac-eo5R9vyChx24LfQWa-3ngQkfy3_gPMcaVha2g596t2XBYh_E9C7n1P6NLpstu2K00E--VtslJY-hK6Pq_gplFUU40C9ew4uEGivWFjEJViFRrobGLvKJnWAH88vggxygwWJP3NLAhMPbi2QREx7NA-wa4n_jZpP69uVNy6fWc7q3UxuqUz8r8_1hKFwnYyjAlUswn59xZ13-GL01ss5lURvrL0wnH57Z_2ni-pqDMf1c3cnGf1XjbW6aCVlhwe4K-VSU4QpVDXElarakBRShEZRx68SkQ4FFtxdZl-iQlBI0Bu6CFjU61TkutO7UncHeXU_-5PU5zA2fTbLykz33TD4IXRJUtjVEWWALLlQgcJH_BDH8-XNqqK4OPF8kEKTvBQpHqAxmwTKe9zQreBlj0ZMnHcLvuO3gnXTb0ely00EomK5hPucFJByWp7jdWp6Tk7C9AReqXAJTavFTVQi7FsixlVxAl58RBwJ6R54NOmDfuU9lebizBlAOJtUVQsUioVxL94ancTujHWqVa_Z72W7aGZ-_qZnPjZ4SwCzLZeSTKLJt9Nslkua-K9jm34O3M7FagzeSkuHLd2DHke3WN-Vr4abROTQrv8HIu-eTFO_NW-vJ2DLy4pNJeQxThWQ7pRBJyp4QG5-pHN14HxQEmp11oJm9aSgCTcs5VIGzaVCO4H7rm7i5tGs5NPjCXKuJwwbG5gUNlwaVbmGhSTpe3qjK4k0ypHZUJO6j2ywJxonc3SpX2m2BMBdYVF5HyDP4YbBseoFJOrfT0TUauQaJY-jgEohDyLjAKUnHLD4di-az_-fTyjmIBifsqf982eeAnClyATCBKbOc1T3e1RA2UarGTozjENyr9hIxlZgjFs97HcUJV4g1JPF9RxEnUyfFUiv7CgSxfel1cnUXOhy3A66t3-ILn2bILY93vXPz-doA8w2ZwT-KTf7u2EW5iSidY5pkfhq8V5kdgzweNrcBNlSDyGFzlp09dMS0MfmtJHqeb77_OSQsk-WzZEVQA3URJI2FYXL5WpmkdWi0ZOt7TrYSHxlvwkM3CplNq0FO-dp7Rs5pn9pJ2dz5g7e1I8ndJk5m0EhnfTz5tCXdwQe8Tc9c5XQd49Fp5cOkBiDVGF9HY4Gp-hwWCQwMpHg2Df36b5i0gX1V7QrJrtT6KW9prB-A0gZXUTV3MiGxr4zU42XRYowSDGEt7ip24_AUUj96xnLvGsvR8Yj3N-X8nmHwWkC9R1ena1ZDJGeoaLCZzDWoqvkueCGHeV2N-wEjUWkPRsi1aUyJbgSRPWmls_5Di86Qymbq5OVLdqiYg6-UlaXUceHrHVi7tbG8EAbZIPF2HSL51ad66_Te16uhvqcr7cG-ItKVONqh-AToJFkFMU2iK3x50zuCNRZNfaHnP8gQkWjpFVoHojC88QU_4skewc_QmTQaYz7VeOiGaJN5HbaAxL-SeeZA74w14Lk7Ajl_B1swXeZIRAY6_VT1upImLNEaiQD6T5lJ9JCToczVdGLeavEH44RTqMpTDl2DKcuvKTkuDLsjlZhD1_9WRw41lWVYkX0Wc_UXca22k0iUxn0Gg1cdeZUBOcGtjine8ihT6fWpFZnkBr9Bl5-qgV6prq57Ci0vdHGBzC_sI_bUQPcQ0YjYDBcH4UBsShrZI8owr6rUWB1jyP0ZfoeFq6QVjTkQlRaegEIOqqcFz2WoRUXiQfnBfi0Oo2mF4sZ4WgofQ4wLYtl1pqiAtVpJr2A_F8-JNR9j8Mv_dY9DcYqMfj8uUrX9M4JoS_Uub8t0we-oYqL4n7zIvw4Qz0xi2MpsRIY9qSCCtBaAXdWlcT6YX2ZzWah7TKKxxohLP7CrxaF__p2cC_z8jyts2OQGGaR8IbgExIgBU8GMGS3I9eKIYAFBp3m8PZsOMHm7Tg8izAmZb7iOwUXwdtDmW-TrDtbHBGSlldO2khLO-Ki3p4KRlqW0R7Ci1zwuATJ18QN-Ea3tU_UA25o00psiyiiqdwpnRauI1WetaAk0YQibcOS3SZivSC_prh1aUU4iK8fKAeNdBgMXyy5IPOGj1G3tNpDl_6DVB7RSrdrYwfW7ToGRJGEkL40oiMI6GqAJDcGtxgovOWxHi5EbUqrYpyYshpS134d9YENyBkYllHyIxK9q0YwfTSlhsq9po3sg9g5_sNlX9VseZkX2jVfOqfRti-X4iX7k44WTTizWGkTzQ1lHKY5r1V95pCAkHNOYjJSbCE8Hj1KDSVyK0cliiASuP1Hk8dnM68irwKQQvJpSk9ymxRHzoJ4hfdusIhRFNNz4eQqJoZCj1L3RxUQ6GqIqLzOzKtJiDsJmEEOT4_gadb-chFEqqn-U5Tf3GmBvNz8mO7v6lwhHaqTlP80o6DYbACsaYS2SFZI8oa-ZKz3PzDYz2RWfuxvo0Ogbgw8cmOWpnQPOIcf0YrfJnTciZ4gx780_WXIPCrKsmneuPsuTa6IHvZAHaIuc3RENt1HvF0R_BzBGmT8BHdUvc8G4iwZcJG1TsnnNChr8fAzeuDAOUMOmIVKmQWvth3EAOPgVXZ0q42luwErg0L9ZdUVDHehgDurbAPXIs4b1HvDvp2fFKibQ7abmsZywrpa6BlXVftkeUdR2NgSeOUXl4mX6J8RQbX0FTpiTtSpnDc_3Fh7WKlKpO21bSEWLsjxZ3I4OjQ7JusRPYxsj9HixyBmIrKIe_nQWuZi3Cuq_YSxVf6M_o19MFMceyUt9Ea6Hshgs3vp6fbA_Ow5I8vaL4fer0EviQrsP30R4Ciyjh2yYMqYAgfuP6Zhjn-boFm1Wf8jDzWk7EZAx_x4hzBLPtjtQdPJbke6Hmi5lZx1cDmILDJeaa9xIGbkibnjZCQvsvqk62P3742Clsl9fOKkXlgLJDywTe2o4MruFfMndqOYDYlhq5BtwefqE2qNrFuizUeT0c4-TAwM8IIS4CB0"},{"domain":"rewards.bing.com","hostOnly":true,"httpOnly":false,"name":"_C_Auth","path":"/","sameSite":"unspecified","secure":false,"session":true,"storeId":"0","value":""},{"domain":"rewards.bing.com","hostOnly":true,"httpOnly":true,"name":".AspNetCore.Antiforgery.icPscOZlg04","path":"/","sameSite":"strict","secure":true,"session":true,"storeId":"0","value":"CfDJ8LfTkwiAHdVDsG3ePT4u9-pN5O6SX5Vepsc1IgBQocMW5tf5MPbz25aBxoInDkspOOhvLQlUdktB_dsNrVYmdzkZH4PO92uX4Z0wng1scQmVgd5RGg57gK-ZeqJoqK_j52XBSjZALL9tsAENntWIdEU"},{"domain":"rewards.bing.com","hostOnly":true,"httpOnly":false,"name":"GRNID","path":"/","sameSite":"no_restriction","secure":true,"session":true,"storeId":"0","value":"02e50f6f-5b3b-40ca-84d1-87bf70b5ffca"},{"domain":".bing.com","hostOnly":false,"httpOnly":true,"name":"_EDGE_S","path":"/","sameSite":"unspecified","secure":false,"session":true,"storeId":"0","value":""},{"domain":"rewards.bing.com","hostOnly":true,"httpOnly":false,"name":"BCP","path":"/","sameSite":"unspecified","secure":true,"session":true,"storeId":"0","value":"AD=0&AL=0&SM=0"},{"domain":"rewards.bing.com","expirationDate":1783185381.599047,"hostOnly":true,"httpOnly":false,"name":"MicrosoftApplicationsTelemetryDeviceId","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"21573e14-89c5-4c95-84b5-74dfbe24dc52"},{"domain":"rewards.bing.com","expirationDate":1783185381.599169,"hostOnly":true,"httpOnly":false,"name":"MicrosoftApplicationsTelemetryFirstLaunchTime","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"2026-01-05T17:16:21.598Z"},{"domain":"rewards.bing.com","expirationDate":1767635181,"hostOnly":true,"httpOnly":false,"name":"webisession","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"%7B%22impressionId%22%3A%220b7ea9b7-c7d7-4b2b-906b-1e01a63c4e3a%22%2C%22sessionid%22%3A%22638ff32e-c00f-42db-a739-f3dd644155da%22%2C%22sessionNumber%22%3A31%7D"},{"domain":".bing.com","expirationDate":1767719782,"hostOnly":false,"httpOnly":false,"name":"_uetsid","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"e9b66230ea5511f0bda63f3330e085bf"},{"domain":".bing.com","expirationDate":1783185382.07324,"hostOnly":false,"httpOnly":false,"name":"_uetvid","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"49ce6a30be2c11f0840b6321b501c897"}]
'''

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/usia', methods=['GET', 'POST'])
def cek_usia():
    if request.method == 'POST':
        # Ambil data dari form
        tahun_lahir = int(request.form['tahun_lahir'])
        tahun_sekarang = datetime.now().year
        usia = tahun_sekarang - tahun_lahir
        return render_template('cek_usia.html', usia=usia, tahun_lahir=tahun_lahir)
    return render_template('cek_usia.html', usia= None)

@app.route('/scrape')
def scrape_bing():
    # Menggunakan API Endpoint yang lebih reliable untuk mengambil data User
    api_url = "https://rewards.bing.com/api/getuserinfo"
    
    findings = []
    poin_text = "Tidak ditemukan"
    page_title = "Bing Rewards API Scraper"
    
    try:
        # Konversi JSON cookie menjadi dictionary untuk requests
        if not BING_COOKIES_JSON:
             return "<h1>Error: Cookies kosong</h1>"
             
        cookie_list = json.loads(BING_COOKIES_JSON)
        jar = requests.cookies.RequestsCookieJar()
        for cookie in cookie_list:
            jar.set(cookie['name'], cookie['value'], domain=cookie.get('domain'), path=cookie.get('path'))

        # Header yang menyerupai browser asli sangat penting
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://rewards.bing.com/",
            "Origin": "https://rewards.bing.com",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/javascript, */*; q=0.01"
        }
        
        findings.append(f"Menghubungi API: {api_url}")
        response = requests.get(api_url, headers=headers, cookies=jar)
        
        findings.append(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                findings.append("Berhasil parsing JSON response.")
                
                # Simpan response untuk debugging
                with open("debug_api_response.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)
                findings.append("Disimpan ke 'debug_api_response.json'.")
                
                # Logika ekstraksi poin
                dashboard = data.get('dashboard', {})
                user_status = dashboard.get('userStatus', {})
                
                if 'availablePoints' in user_status:
                    poin = user_status['availablePoints']
                    poin_text = f"{int(poin):,}" # Format dengan ribuan separator
                    findings.append("Ditemukan di dashboard -> userStatus -> availablePoints")
                else:
                    findings.append("Key 'availablePoints' tidak ditemukan di path standar. Coba regex pada seluruh JSON.")
                    import re
                    # Fallback: cari pattern "availablePoints": 1234 di string JSON
                    json_str = json.dumps(data)
                    match = re.search(r'"availablePoints"\s*:\s*(\d+)', json_str)
                    if match:
                        poin_text = f"{int(match.group(1)):,}"
                        findings.append("Ditemukan melalui Regex Search di JSON.")
            except json.JSONDecodeError:
                findings.append("Response bukan valid JSON. Mungkin session expired atau redirect ke login page.")
                # Coba simpan text nya
                with open("debug_api_error.html", "w", encoding="utf-8") as f:
                    f.write(response.text)
                findings.append("Disimpan response body ke 'debug_api_error.html'")
        else:
             findings.append("Gagal mengambil data dari API.")

        return f"""
        <html>
            <body style="font-family: 'Segoe UI', Arial, sans-serif; padding: 40px; background-color: #f4f4f4;">
                <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                    <h1 style="color: #0078d4; margin-top: 0;">Bing Rewards Points</h1>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <span style="font-size: 16px; color: #666;">Total Poin Anda</span><br>
                        <span style="font-size: 48px; font-weight: bold; color: {'#green' if poin_text != 'Tidak ditemukan' else '#red'};">{poin_text}</span>
                    </div>

                    <div style="border-top: 1px solid #eee; padding-top: 20px;">
                        <details>
                            <summary style="cursor: pointer; color: #0078d4; font-weight: 500;">Lihat Log Debugging</summary>
                            <pre style="background: #f8f8f8; padding: 10px; border-radius: 6px; font-size: 12px; margin-top: 10px; overflow-x: auto;">{'<br>'.join(findings)}</pre>
                        </details>
                    </div>
                     <p style="font-size: 12px; color: #999; margin-top: 20px; text-align: center;">Checked at {datetime.now().strftime("%H:%M:%S")}</p>
                </div>
            </body>
        </html>
        """
    except Exception as e:
        import traceback
        return f"<h1>Internal Error</h1><pre>{traceback.format_exc()}</pre>"

if __name__ == "__main__":
    app.run(host='127.0.0.1')
