#!/usr/bin/env python3
import requests
url = 'https://www.realtor.com/realestateandhomes-search/Escambia-County_AL/pg-1'
headers = {
    # 'cookie': '__ssnstarttime=1571404219;_ss=1366x768;__split=27;threshold_value=17;automation=false;__ssn=8e80592a-3941-4bc4-9f1d-9306b2f60826;split_tcv=119;clstr=v;split=n;clstr_tcv=28;__vst=8c80f913-4a5b-4f36-beb9-b887a2d12bff;_gat=1;reese84=3:pfLfkl9SgJYJ2gw7117VSQ==:/1JmPB1toS1CZYOYN7c1AOK+kyUp8VJX7geyOpxSPZRCewYB0RE4DTF0k9jFEXDRReyQFkSmw+7U+bUavfWHBqVuFw4PIZYyvYAL0Mgp7l+YI+LHYrKrI+e7wHE+i904HnXAW4C6PR3bcj44eqWq5As40Y5p8UlTF9QjCtvmR/GpaBIQp2BGFwisd1bB9FLSrELVv4MLi7Xszeb5qolvrLIFfHUgxMmyyGT1ugDHXhSzwmgkMjW+TxAfBTxUEiGDEDc9y1MgisDtWyHMgfazqfm8KewFs/ezutDktMeEe4lcM0UswwPDGSE0hpMFliek2HoEfuhIImCTgIGO1/zpmOlM2l5J99c+cLF4f2yVrkDvl8FgaYkR6W0laCmkYWFsHhLUfIbFPHrCwD+G5nzqvTEchwkMCm618Wv7YLACivE=:+4sm5yCHyy+vZk+PYEfJh49dw8JV2RmAdbMOzGz+eEw=;_ga=GA1.2.498560712.1571404224;bcc=false;bcvariation=SRPBCRR%3Av1%3Adesktop;header_slugs=gs%3DEscambia-County_AL%26lo%3DEscambia%26st%3Dcounty;ab_srp_viewtype=ab-list-view;srchID=22be2515f17a4c23879eb4b72b612a8c;AMCVS_8853394255142B6A0A4C98A4%40AdobeOrg=1;__gads=ID=fef4d288b271740e:T=1571404224:S=ALNI_MZp3ttmodBY2s6glhajujCm-FLGZA;ajs_user_id=null;ajs_group_id=null;_gid=GA1.2.1235009098.1571404226;s_ecid=MCMID%7C43469670477918190300407094417458682770;AMCV_8853394255142B6A0A4C98A4%40AdobeOrg=-1712354808%7CMCIDTS%7C18188%7CMCMID%7C43469670477918190300407094417458682770%7CMCAAMLH-1572009027%7C11%7CMCAAMB-1572009027%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCCIDH%7C-549291961%7CMCOPTOUT-1571411427s%7CNONE%7CMCSYNCSOP%7C411-18195%7CMCAID%7CNONE%7CvVersion%7C4.3.0;_tac=false~self|not-available;_ncg_sp_ses.cc72=*;_ncg_id_=45b71348-5e1f-4c0f-8df8-6562a976bc91;_rdc-next_session=SldnY2FHS29NTkcyZXJoblgrUGlkcE5vanE4eHU5SnNXd2RlbUJtdC9Fdytha3hqdjc4RDBCRG9oMnBFMG5paGVXYVlYSUNtYWV3anBCNWIwSkFFTzkyejNsR291TXRpUnloQW9VRS9jNnV0ZERqS3RkWWRVMk54SGYzR01sNVdUWWRDTk83OUtNWWROSGh0VUcwbjVURFhYMWthVDdHbnpnY0x6dVdhLy9HZTVKRHRQM1N4VUFrYVFnZVNLSUJCTGxaU1JaTmcyNm84NWw0TFBwaTJxTEpiRDdVbUsrd0REaWQ1N1owOGprcVlIZStFQmozb0lsSVpCSTMyUHFrb3VXNWliRHBmWXhQVE5DNTYyeFFCQTN3MDdwK0VlaHNWajJsc1pVcGQ0dWlZOU5qb2ZBbzJuTVA1Sm9tM1NnZ2cydVc1S0pJQ1hQQ1lFWWpUUnZmZTVHNjNtTDNjU3FHU3hQODZTYWQ2L0RzM0ozYXRaTU52Z3V5dE85QlBXSmFLQ1pxbkZaRXBPTzlXeVVTWmtZRE1GcTN4aHVDTlZjWTdYRFhsbXFrb3A0SmhHMjcyVFlNem9rSlZ6RVRrSTRTY3ZQRVA2ekhhM1NWZjQvei9uOCtFcURxMElaQlJ0SEhVbDRJWVJUaERrMjRCSjQ5R0xQakJLditWNVV3SS9ha2VqV2xqYklUbEdIMEpkOEVJMWdKQVQyU01NcGJQOU9BclVsZEs5Vjk4eGs4UlUxa3pZQi9rNWhwM1M1YlFqOFJoaEpxaTgyQzI2UjJ1bXU0WjVjUmFvbE96QjlWUTEzMVNtcDZ4YmNNV0dHZElKTU9uZFBEUXVVd3VXMERDc3NlZS0tNWV6a2pSVUlzY0xFRzk4UFhCbWozZz09--77aea72c9b10723d4f6ac8899084c0f500cb939a;_ncg_sp_id.cc72=45b71348-5e1f-4c0f-8df8-6562a976bc91.1571404279.1.1571404280.1571404279.c5f39139-6a99-4eaf-a61c-076256211996;__qca=P0-183496167-1571404285816;QSI_HistorySession=https%3A%2F%2Fwww.realtor.com%2Frealestateandhomes-search%2FEscambia-County_AL~1571404416102;userStatus=new_user;criteria=loc%3DEscambia%20County%2C%20AL%26locSlug%3DEscambia-County_AL%26lat%3D31.126123%26long%3D-87.16162%26status%3D1%26pg%3D1%26pgsz%3D44%26sprefix%3D%2Frealestateandhomes-search%26city%3DEscambia%20County%26state_id%3DAL%26ns%3D1;ajs_anonymous_id=%2227d04b2c-85d8-47f7-b7ee-8387bb0619e7%22;__edwssnstarttime=1571404420;_ta=us~1~89df68bc35032d48c293adce8574aa42;_tas=lfkx2xmydxm;',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
}
proxies = {
    'https': '163.125.253.205:9797',
    'http': '163.125.253.205:9797'
}
r = requests.get(url='https://www.baidu.com/', headers=headers, proxies=proxies)
print(r.text)