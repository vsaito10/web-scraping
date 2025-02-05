import datetime 
import pandas as pd
import requests

class buyback:
    def __init__(self):

        # Dicionários dos cookies
        dict_cookies = {
            # Cookies página 1
            'cookies_1': {
                'dtCookie': 'v_4_srv_28_sn_7772C83367A57C58554BC5A0DD8493E9_perc_100000_ol_0_mul_1_app-3Afd69ce40c52bd20e_1_rcs-3Acss_0',
                'TS0134a800': '016e3b076f3a37b3c1572dcbeea95ba2c9f51626189129677bc461db18c444257f6c70076685529d68724a19f30dbed7462583c088',
                'rxVisitor': '1738322613498U4O58MVS6EOUI43V3QAPBUE9AA0KP93T',
                'TS0171d45d': '011d592ce17c36dfb21981abb888c7b109818aaae2283b1f67cb01c20d79e1488936e3fd73529eea5b37bfc4cabd9f54660543662b',
                '__cf_bm': 'PmJBAAWr09SqEXnzLpEiJgbVmdmd2kDIo9ObzuoI9ds-1738374604-1.0.1.1-8VB2ey7qf2I28xViLiUwA0RJvyKUA7NF8UZ5U5tou9VPxQTM4vkl8XbMsHQH0TtNzPLq8_iMXjjC1dLuCoKAfg',
                'dtSa': '-',
                'TS01871345': '016e3b076fdecf0d20ff67d211677c81329e1154c17e65de27e9fca33f407aa8e59b72c7a2489218b5129b839fac8313bde37d5b0e',
                'cf_clearance': 'NTQ8CBzLz.ZtFY30GroGKzueaOSj4OAm4UOjj377ImY-1738374606-1.2.1.1-O6jLhN6A_hLYcIq9_pC_HoWANRt.OzTdSPhx9QljHPqqsnsb.8w18Sms6hc4pnEYoP2F3wMxBcIzBhvjxUlwVOVhG9fS9zX5w2uppMEl_Hpovm2u4MyFI.dh4vSuFvPcGuukod4HzP9GwDIZ_X8ICyv83lpPxXVIPkDc3PXglbcs7WOEHBh4pJZ3qbeBNczDO4w1jJN3UwXXb9QlOfrdSg5pDHN0nA5FNbh.rW5lw7e0LsSbFfX9KEuKZ2MEY4DGBJWOW15vWIXg7GNOZKugR0liy.txtYdh.4pqBFWcfEs',
                'BIGipServerpool_sistemaswebb3-listados_8443_WAF': '1329140746.64288.0000',
                'dtPC': '28$174682776_87h1p28$174682982_140h1vGCTMWPWCRPCCLRVUKLLHJKHNSHVRTAIK-0e0',
                'rxvt': '1738376482994|1738374561029',
            },

            # Cookies página 2
            'cookies_2': {
                'dtCookie': 'v_4_srv_33_sn_76EF270DB99B9F2DFDD25CE7443B193D_perc_100000_ol_0_mul_1_app-3Afd69ce40c52bd20e_1_rcs-3Acss_0',
                'TS0134a800': '016e3b076ff209bbc93f9b7db1f0d49be631132f17dfc874d374d43078a3e0ae6268ec31e405025baf7c325362897f0451fd0b23cd',
                'rxVisitor': '17384415824942VP8SUIC1F5NGU3S4LRAK2QHNAAB5LP6',
                'dtSa': '-',
                '__cf_bm': 'meqy8ELt.6lJpw3qa6kU3F0sFaAZ9jYiM8ilvm1s.WY-1738451946-1.0.1.1-ZbDxqsIrBbMdGAzlqF.YKdSKpSrM.NN9ElNDamu7qKnUna4LD6N.9Eo.g9GqSl48uID7w01VNKN1r2iyLJRCGg',
                'TS0171d45d': '011d592ce1cdbb15c0ecf48ec6e2b731f82daee311800695e6b65addd7334b516a1c2ccd0b408d6eae9cc489a29212dc5ef92a6abc',
                'TS01871345': '016e3b076f35f446a36fc729584f6e123f198434cf692a7789232dadbc27873535aa20f65ecf4206e505ab2b130dff7ff4e57b60e3',
                'BIGipServerpool_sistemaswebb3-listados_8443_WAF': '1329145866.64288.0000',
                'rxvt': '1738453952419|1738450153034',
                'cf_clearance': 'bgQXiYrJKIi9CkYmnXfw1R3zo2scIcdvGqdI2K8TBbg-1738452196-1.2.1.1-S2YSNVyTbVZjEywmz_lqT7D0BXayyWb5OCZFmVFrLZc9jFL9UixByIb3vA17aWhQRusBvgf8KmdryexCuvqAyJ5Em7DC6OjdM0xCFzFo_Da8PCKXJurCeq5Ngx3DI3FvJNoOADmudh3TkkR8YxdKYs1Sg9sRBz0drNqlYO82jQmYTVKjohkrAkBbig8S8rvPK2ONPNC6UjVbcPqLBctxpnOJD45J9iMFFx45H0zis2AFpAm6H6i_M3wD6UOeyIB7e2WKb25U.nJ0K3Ax0v67h3NDHzko9AX__PZ8l6aIfmc',
                'dtPC': '33$252152077_406h-vBHFCEDJVFCUKCFSNJVCCSKBDUTGDOOOU-0e0',
            },

            # Cookies página 3
            'cookies_3': {
                'dtCookie': 'v_4_srv_33_sn_76EF270DB99B9F2DFDD25CE7443B193D_perc_100000_ol_0_mul_1_app-3Afd69ce40c52bd20e_1_rcs-3Acss_0',
                'TS0134a800': '016e3b076ff209bbc93f9b7db1f0d49be631132f17dfc874d374d43078a3e0ae6268ec31e405025baf7c325362897f0451fd0b23cd',
                'rxVisitor': '17384415824942VP8SUIC1F5NGU3S4LRAK2QHNAAB5LP6',
                'dtSa': '-',
                'BIGipServerpool_sistemaswebb3-listados_8443_WAF': '1329145866.64288.0000',
                '__cf_bm': 'meqy8ELt.6lJpw3qa6kU3F0sFaAZ9jYiM8ilvm1s.WY-1738451946-1.0.1.1-ZbDxqsIrBbMdGAzlqF.YKdSKpSrM.NN9ElNDamu7qKnUna4LD6N.9Eo.g9GqSl48uID7w01VNKN1r2iyLJRCGg',
                'TS0171d45d': '011d592ce1cdbb15c0ecf48ec6e2b731f82daee311800695e6b65addd7334b516a1c2ccd0b408d6eae9cc489a29212dc5ef92a6abc',
                'TS01871345': '016e3b076f35f446a36fc729584f6e123f198434cf692a7789232dadbc27873535aa20f65ecf4206e505ab2b130dff7ff4e57b60e3',
                'rxvt': '1738453713634|1738450153034',
                'cf_clearance': '5hUBmEDiLr6mAuHG1Ipoxwy1IiRzv5La7oYgu30OsMc-1738451957-1.2.1.1-KUpis1yaUxikBR5KS._vfzymiIqs5wp6mLoaUL3A.vqGhjwTXp2t244trkG9PIdl6eiG5WbFCWBdGIpRSkETfCcAhP83SF30Q22Eiz7LrbI33wTe3IaUpJxK62.J.xpX0hNPhvqTp4Cdeo9j0kPXzA6WYIY82zaZjB2rotjqMlg9x4UDrh2tZ1qiN1Lj5PPsssBBQA1p3MxeCW83ngy9mDBmP96XDS_HmwJmtqkeudZB3xxIrVpcBaZG_fclgP8GlguzoFabI8tC8LYnO2tRV0km_ugq3sBFEDnTSepCM10',
                'dtPC': '33$251913137_37h-vBHFCEDJVFCUKCFSNJVCCSKBDUTGDOOOU-0e0',
            },

            # Cookies página 4
            'cookies_4': {
                'dtCookie': 'v_4_srv_33_sn_76EF270DB99B9F2DFDD25CE7443B193D_perc_100000_ol_0_mul_1_app-3Afd69ce40c52bd20e_1_rcs-3Acss_0',
                'TS0134a800': '016e3b076ff209bbc93f9b7db1f0d49be631132f17dfc874d374d43078a3e0ae6268ec31e405025baf7c325362897f0451fd0b23cd',
                'rxVisitor': '17384415824942VP8SUIC1F5NGU3S4LRAK2QHNAAB5LP6',
                'dtSa': '-',
                '__cf_bm': 'meqy8ELt.6lJpw3qa6kU3F0sFaAZ9jYiM8ilvm1s.WY-1738451946-1.0.1.1-ZbDxqsIrBbMdGAzlqF.YKdSKpSrM.NN9ElNDamu7qKnUna4LD6N.9Eo.g9GqSl48uID7w01VNKN1r2iyLJRCGg',
                'TS0171d45d': '011d592ce1cdbb15c0ecf48ec6e2b731f82daee311800695e6b65addd7334b516a1c2ccd0b408d6eae9cc489a29212dc5ef92a6abc',
                'TS01871345': '016e3b076f34a422c5573c731ca66a2b7157c4810c035638d07a7c55ab6c5b01f8c44ddbbff9190f0c8d1faf43ea9e312d0188ccf2',
                'rxvt': '1738454143792|1738450153034',
                'dtPC': '33$252343314_525h-vBHFCEDJVFCUKCFSNJVCCSKBDUTGDOOOU-0e0',
                'BIGipServerpool_sistemaswebb3-listados_8443_WAF': '1329145866.64288.0000',
                'cf_clearance': '09bjJNvTLUbvEsoaklyPqDMvLJpK40_C7noERXpsx8Q-1738452387-1.2.1.1-BuO7wR8S1YOa1dtbYBlxduE2KixyqIwelJI8Nfqg_Wcs3xS3iLl6fbOPFTqwusVG1ggPjuGO_cdrpNlJhk5qXghTHoTkihHUV4CcGWhtXWSjPH1hXimmR52rs6ikeg0NhcMr1BTxV.FHNGkylwqU0hU7oVgzhbIqn5W9O3YbJ_KMxk.6fBfnNY3px.XgaXy5forfW5qLAmFsyXm0nduhNOcTA2VhOLS00JC1qFTmZIXJ9RnhwYXZU3D5.JZf11GVTvoIbTbB818X0MMwMaaPsAUGQe_sGEBGCJGU_.rx2IU',
            }   ,

            # Cookies página 5
            'cookies_5': {
                'dtCookie': 'v_4_srv_33_sn_76EF270DB99B9F2DFDD25CE7443B193D_perc_100000_ol_0_mul_1_app-3Afd69ce40c52bd20e_1_rcs-3Acss_0',
                'TS0134a800': '016e3b076ff209bbc93f9b7db1f0d49be631132f17dfc874d374d43078a3e0ae6268ec31e405025baf7c325362897f0451fd0b23cd',
                'rxVisitor': '17384415824942VP8SUIC1F5NGU3S4LRAK2QHNAAB5LP6',
                'dtSa': '-',
                '__cf_bm': 'meqy8ELt.6lJpw3qa6kU3F0sFaAZ9jYiM8ilvm1s.WY-1738451946-1.0.1.1-ZbDxqsIrBbMdGAzlqF.YKdSKpSrM.NN9ElNDamu7qKnUna4LD6N.9Eo.g9GqSl48uID7w01VNKN1r2iyLJRCGg',
                'TS01871345': '016e3b076f34a422c5573c731ca66a2b7157c4810c035638d07a7c55ab6c5b01f8c44ddbbff9190f0c8d1faf43ea9e312d0188ccf2',
                'BIGipServerpool_sistemaswebb3-listados_8443_WAF': '1329145866.64288.0000',
                'TS0171d45d': '011d592ce10bf6b8c9ffa149856bab443308113a7e3693865a2b941bef076b43f52559b07e24e82e6865a53022f9417de9223839e1',
                'rxvt': '1738454227591|1738450153034',
                'dtPC': '33$252427213_234h-vBHFCEDJVFCUKCFSNJVCCSKBDUTGDOOOU-0e0',
                'cf_clearance': 'F92v15zJ6X3nVP3SgT2BW4IAYmzg2wYmQOlLHPc1tfc-1738452471-1.2.1.1-9Ve.H5qGjYD20l0EUd5iAD_07xi331OH1sPkFpuGbYJvLhAaRKWb8IKMaLpNf5Zxu2mVu.eG4Oq6U76dARGR0uOSn8qvnliDinHSacGauGHdcAHO62NYKawJeaFt3ASY0pWOtUOz0nwz9_uENoGWaRfCGDO3P3mX6emNatoiOZvxyFiQEKtl8zvJVVoBEGotx3j2E9O9KHLDR4KztOV0nryeI0HWhSWDEV3_uWAZcCj96W.Nkv5Ph2hkvDKFj5WUwtXPyDHFN64YCA4qtXkp7z0jOuXXKhv.VfnIB0tN0hU',
            },

            # Cookies página 6
            'cookies_6': {
                'dtCookie': 'v_4_srv_33_sn_76EF270DB99B9F2DFDD25CE7443B193D_perc_100000_ol_0_mul_1_app-3Afd69ce40c52bd20e_1_rcs-3Acss_0',
                'TS0134a800': '016e3b076ff209bbc93f9b7db1f0d49be631132f17dfc874d374d43078a3e0ae6268ec31e405025baf7c325362897f0451fd0b23cd',
                'rxVisitor': '17384415824942VP8SUIC1F5NGU3S4LRAK2QHNAAB5LP6',
                'dtSa': '-',
                '__cf_bm': 'meqy8ELt.6lJpw3qa6kU3F0sFaAZ9jYiM8ilvm1s.WY-1738451946-1.0.1.1-ZbDxqsIrBbMdGAzlqF.YKdSKpSrM.NN9ElNDamu7qKnUna4LD6N.9Eo.g9GqSl48uID7w01VNKN1r2iyLJRCGg',
                'TS01871345': '016e3b076f34a422c5573c731ca66a2b7157c4810c035638d07a7c55ab6c5b01f8c44ddbbff9190f0c8d1faf43ea9e312d0188ccf2',
                'TS0171d45d': '011d592ce10bf6b8c9ffa149856bab443308113a7e3693865a2b941bef076b43f52559b07e24e82e6865a53022f9417de9223839e1',
                'BIGipServerpool_sistemaswebb3-listados_8443_WAF': '1329140746.64288.0000',
                'cf_clearance': 'INbMZX0bOFhveZC1kLK59LgavsMJzQMGomYwfbz4Eao-1738452543-1.2.1.1-Cs8SoacZUJ1oMb0bOOm026Z._Li5RCXB7e6dMgf9T3a3yq_tJNKh3eVBhl8f35qf5x2iiJ_FiHmZaf3IpNZjy2Qvn4Lt9Q.wywggX5TPHZwFFVXgyFadu7YeJbMlhuZrbC09fdU8qfZRVg._umHzd0Xy0wB4L78eGGDC9zti1gMo_joZC4KayGQ6wYaYw9rz7vnS43OCGSK_TVbmKpWJp3BQjDzuoO.w.CypT2F9Kmz1ZdST78jwh7IqpdhpzImXt.sQOvt4ujggZ9.ouqxxyBHCiDtUobXD.M9mb7u56Ng',
                'rxvt': '1738454299689|1738450153034',
                'dtPC': '33$252499333_186h-vBHFCEDJVFCUKCFSNJVCCSKBDUTGDOOOU-0e0',
            },

            # Cookies página 7
            'cookies_7': {
                'dtCookie': 'v_4_srv_33_sn_76EF270DB99B9F2DFDD25CE7443B193D_perc_100000_ol_0_mul_1_app-3Afd69ce40c52bd20e_1_rcs-3Acss_0',
                'TS0134a800': '016e3b076ff209bbc93f9b7db1f0d49be631132f17dfc874d374d43078a3e0ae6268ec31e405025baf7c325362897f0451fd0b23cd',
                'rxVisitor': '17384415824942VP8SUIC1F5NGU3S4LRAK2QHNAAB5LP6',
                'dtSa': '-',
                '__cf_bm': 'meqy8ELt.6lJpw3qa6kU3F0sFaAZ9jYiM8ilvm1s.WY-1738451946-1.0.1.1-ZbDxqsIrBbMdGAzlqF.YKdSKpSrM.NN9ElNDamu7qKnUna4LD6N.9Eo.g9GqSl48uID7w01VNKN1r2iyLJRCGg',
                'TS01871345': '016e3b076f34a422c5573c731ca66a2b7157c4810c035638d07a7c55ab6c5b01f8c44ddbbff9190f0c8d1faf43ea9e312d0188ccf2',
                'TS0171d45d': '011d592ce10bf6b8c9ffa149856bab443308113a7e3693865a2b941bef076b43f52559b07e24e82e6865a53022f9417de9223839e1',
                'BIGipServerpool_sistemaswebb3-listados_8443_WAF': '1329140746.64288.0000',
                'cf_clearance': 'cbLgmzjWkRLuKnE5PdAoEa9z9fRW1cVOXBxx62abwyY-1738452627-1.2.1.1-wdzQBzKUN7swJ6rqRR8FaLWXk4uGXc3fbkrjOAIL4XIIE05kkbiTDNQNWkHWDAHCRNjqXbF9prNKkDyr2_qsqdRuR9iocmWHC7OmFy7Qq351TvsdoGl27UQZMKfnmD4EQxR6dnfOPIIJfhW0nthG_dxkzRuvHg4PHsGtitJRj3.UKlK9BQxUxDRyKBOvy7tlIur_7B5GjYlw_R.1tgUY05hEERxkaRLkzSXadobSy3VTic2qmt9GOfw8gaIDOveQ1MVa6sx3KETwMPA7zQiuMn3egI0Bqh1GtsuoYoajmUE',
                'rxvt': '1738454383981|1738450153034',
                'dtPC': '33$252583550_476h-vBHFCEDJVFCUKCFSNJVCCSKBDUTGDOOOU-0e0',
            }
        }

        # Dicionários dos headers
        dict_headers = {
            # Headers página 1
            'headers_1': {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'pt-BR,pt;q=0.7',
                # 'cookie': 'dtCookie=v_4_srv_28_sn_7772C83367A57C58554BC5A0DD8493E9_perc_100000_ol_0_mul_1_app-3Afd69ce40c52bd20e_1_rcs-3Acss_0; TS0134a800=016e3b076f3a37b3c1572dcbeea95ba2c9f51626189129677bc461db18c444257f6c70076685529d68724a19f30dbed7462583c088; rxVisitor=1738322613498U4O58MVS6EOUI43V3QAPBUE9AA0KP93T; TS0171d45d=011d592ce17c36dfb21981abb888c7b109818aaae2283b1f67cb01c20d79e1488936e3fd73529eea5b37bfc4cabd9f54660543662b; __cf_bm=PmJBAAWr09SqEXnzLpEiJgbVmdmd2kDIo9ObzuoI9ds-1738374604-1.0.1.1-8VB2ey7qf2I28xViLiUwA0RJvyKUA7NF8UZ5U5tou9VPxQTM4vkl8XbMsHQH0TtNzPLq8_iMXjjC1dLuCoKAfg; dtSa=-; TS01871345=016e3b076fdecf0d20ff67d211677c81329e1154c17e65de27e9fca33f407aa8e59b72c7a2489218b5129b839fac8313bde37d5b0e; cf_clearance=NTQ8CBzLz.ZtFY30GroGKzueaOSj4OAm4UOjj377ImY-1738374606-1.2.1.1-O6jLhN6A_hLYcIq9_pC_HoWANRt.OzTdSPhx9QljHPqqsnsb.8w18Sms6hc4pnEYoP2F3wMxBcIzBhvjxUlwVOVhG9fS9zX5w2uppMEl_Hpovm2u4MyFI.dh4vSuFvPcGuukod4HzP9GwDIZ_X8ICyv83lpPxXVIPkDc3PXglbcs7WOEHBh4pJZ3qbeBNczDO4w1jJN3UwXXb9QlOfrdSg5pDHN0nA5FNbh.rW5lw7e0LsSbFfX9KEuKZ2MEY4DGBJWOW15vWIXg7GNOZKugR0liy.txtYdh.4pqBFWcfEs; BIGipServerpool_sistemaswebb3-listados_8443_WAF=1329140746.64288.0000; dtPC=28$174682776_87h1p28$174682982_140h1vGCTMWPWCRPCCLRVUKLLHJKHNSHVRTAIK-0e0; rxvt=1738376482994|1738374561029',
                'priority': 'u=1, i',
                'referer': 'https://sistemaswebb3-listados.b3.com.br/',
                'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            },

            # Headers página 2
            'headers_2': {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'pt-BR,pt;q=0.6',
                # 'cookie': 'dtCookie=v_4_srv_33_sn_76EF270DB99B9F2DFDD25CE7443B193D_perc_100000_ol_0_mul_1_app-3Afd69ce40c52bd20e_1_rcs-3Acss_0; TS0134a800=016e3b076ff209bbc93f9b7db1f0d49be631132f17dfc874d374d43078a3e0ae6268ec31e405025baf7c325362897f0451fd0b23cd; rxVisitor=17384415824942VP8SUIC1F5NGU3S4LRAK2QHNAAB5LP6; dtSa=-; __cf_bm=meqy8ELt.6lJpw3qa6kU3F0sFaAZ9jYiM8ilvm1s.WY-1738451946-1.0.1.1-ZbDxqsIrBbMdGAzlqF.YKdSKpSrM.NN9ElNDamu7qKnUna4LD6N.9Eo.g9GqSl48uID7w01VNKN1r2iyLJRCGg; TS0171d45d=011d592ce1cdbb15c0ecf48ec6e2b731f82daee311800695e6b65addd7334b516a1c2ccd0b408d6eae9cc489a29212dc5ef92a6abc; TS01871345=016e3b076f35f446a36fc729584f6e123f198434cf692a7789232dadbc27873535aa20f65ecf4206e505ab2b130dff7ff4e57b60e3; BIGipServerpool_sistemaswebb3-listados_8443_WAF=1329145866.64288.0000; rxvt=1738453952419|1738450153034; cf_clearance=bgQXiYrJKIi9CkYmnXfw1R3zo2scIcdvGqdI2K8TBbg-1738452196-1.2.1.1-S2YSNVyTbVZjEywmz_lqT7D0BXayyWb5OCZFmVFrLZc9jFL9UixByIb3vA17aWhQRusBvgf8KmdryexCuvqAyJ5Em7DC6OjdM0xCFzFo_Da8PCKXJurCeq5Ngx3DI3FvJNoOADmudh3TkkR8YxdKYs1Sg9sRBz0drNqlYO82jQmYTVKjohkrAkBbig8S8rvPK2ONPNC6UjVbcPqLBctxpnOJD45J9iMFFx45H0zis2AFpAm6H6i_M3wD6UOeyIB7e2WKb25U.nJ0K3Ax0v67h3NDHzko9AX__PZ8l6aIfmc; dtPC=33$252152077_406h-vBHFCEDJVFCUKCFSNJVCCSKBDUTGDOOOU-0e0',
                'priority': 'u=1, i',
                'referer': 'https://sistemaswebb3-listados.b3.com.br/',
                'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            },

            # Headers página 3
            'headers_3': {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'pt-BR,pt;q=0.6',
                # 'cookie': 'dtCookie=v_4_srv_33_sn_76EF270DB99B9F2DFDD25CE7443B193D_perc_100000_ol_0_mul_1_app-3Afd69ce40c52bd20e_1_rcs-3Acss_0; TS0134a800=016e3b076ff209bbc93f9b7db1f0d49be631132f17dfc874d374d43078a3e0ae6268ec31e405025baf7c325362897f0451fd0b23cd; rxVisitor=17384415824942VP8SUIC1F5NGU3S4LRAK2QHNAAB5LP6; dtSa=-; BIGipServerpool_sistemaswebb3-listados_8443_WAF=1329145866.64288.0000; __cf_bm=meqy8ELt.6lJpw3qa6kU3F0sFaAZ9jYiM8ilvm1s.WY-1738451946-1.0.1.1-ZbDxqsIrBbMdGAzlqF.YKdSKpSrM.NN9ElNDamu7qKnUna4LD6N.9Eo.g9GqSl48uID7w01VNKN1r2iyLJRCGg; TS0171d45d=011d592ce1cdbb15c0ecf48ec6e2b731f82daee311800695e6b65addd7334b516a1c2ccd0b408d6eae9cc489a29212dc5ef92a6abc; TS01871345=016e3b076f35f446a36fc729584f6e123f198434cf692a7789232dadbc27873535aa20f65ecf4206e505ab2b130dff7ff4e57b60e3; rxvt=1738453713634|1738450153034; cf_clearance=5hUBmEDiLr6mAuHG1Ipoxwy1IiRzv5La7oYgu30OsMc-1738451957-1.2.1.1-KUpis1yaUxikBR5KS._vfzymiIqs5wp6mLoaUL3A.vqGhjwTXp2t244trkG9PIdl6eiG5WbFCWBdGIpRSkETfCcAhP83SF30Q22Eiz7LrbI33wTe3IaUpJxK62.J.xpX0hNPhvqTp4Cdeo9j0kPXzA6WYIY82zaZjB2rotjqMlg9x4UDrh2tZ1qiN1Lj5PPsssBBQA1p3MxeCW83ngy9mDBmP96XDS_HmwJmtqkeudZB3xxIrVpcBaZG_fclgP8GlguzoFabI8tC8LYnO2tRV0km_ugq3sBFEDnTSepCM10; dtPC=33$251913137_37h-vBHFCEDJVFCUKCFSNJVCCSKBDUTGDOOOU-0e0',
                'priority': 'u=1, i',
                'referer': 'https://sistemaswebb3-listados.b3.com.br/',
                'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            },

            # Headers página 4
            'headers_4': {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'pt-BR,pt;q=0.6',
                # 'cookie': 'dtCookie=v_4_srv_33_sn_76EF270DB99B9F2DFDD25CE7443B193D_perc_100000_ol_0_mul_1_app-3Afd69ce40c52bd20e_1_rcs-3Acss_0; TS0134a800=016e3b076ff209bbc93f9b7db1f0d49be631132f17dfc874d374d43078a3e0ae6268ec31e405025baf7c325362897f0451fd0b23cd; rxVisitor=17384415824942VP8SUIC1F5NGU3S4LRAK2QHNAAB5LP6; dtSa=-; __cf_bm=meqy8ELt.6lJpw3qa6kU3F0sFaAZ9jYiM8ilvm1s.WY-1738451946-1.0.1.1-ZbDxqsIrBbMdGAzlqF.YKdSKpSrM.NN9ElNDamu7qKnUna4LD6N.9Eo.g9GqSl48uID7w01VNKN1r2iyLJRCGg; TS0171d45d=011d592ce1cdbb15c0ecf48ec6e2b731f82daee311800695e6b65addd7334b516a1c2ccd0b408d6eae9cc489a29212dc5ef92a6abc; TS01871345=016e3b076f34a422c5573c731ca66a2b7157c4810c035638d07a7c55ab6c5b01f8c44ddbbff9190f0c8d1faf43ea9e312d0188ccf2; rxvt=1738454143792|1738450153034; dtPC=33$252343314_525h-vBHFCEDJVFCUKCFSNJVCCSKBDUTGDOOOU-0e0; BIGipServerpool_sistemaswebb3-listados_8443_WAF=1329145866.64288.0000; cf_clearance=09bjJNvTLUbvEsoaklyPqDMvLJpK40_C7noERXpsx8Q-1738452387-1.2.1.1-BuO7wR8S1YOa1dtbYBlxduE2KixyqIwelJI8Nfqg_Wcs3xS3iLl6fbOPFTqwusVG1ggPjuGO_cdrpNlJhk5qXghTHoTkihHUV4CcGWhtXWSjPH1hXimmR52rs6ikeg0NhcMr1BTxV.FHNGkylwqU0hU7oVgzhbIqn5W9O3YbJ_KMxk.6fBfnNY3px.XgaXy5forfW5qLAmFsyXm0nduhNOcTA2VhOLS00JC1qFTmZIXJ9RnhwYXZU3D5.JZf11GVTvoIbTbB818X0MMwMaaPsAUGQe_sGEBGCJGU_.rx2IU',
                'priority': 'u=1, i',
                'referer': 'https://sistemaswebb3-listados.b3.com.br/',
                'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            },

            # Headers página 5
            'headers_5': {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'pt-BR,pt;q=0.6',
                # 'cookie': 'dtCookie=v_4_srv_33_sn_76EF270DB99B9F2DFDD25CE7443B193D_perc_100000_ol_0_mul_1_app-3Afd69ce40c52bd20e_1_rcs-3Acss_0; TS0134a800=016e3b076ff209bbc93f9b7db1f0d49be631132f17dfc874d374d43078a3e0ae6268ec31e405025baf7c325362897f0451fd0b23cd; rxVisitor=17384415824942VP8SUIC1F5NGU3S4LRAK2QHNAAB5LP6; dtSa=-; __cf_bm=meqy8ELt.6lJpw3qa6kU3F0sFaAZ9jYiM8ilvm1s.WY-1738451946-1.0.1.1-ZbDxqsIrBbMdGAzlqF.YKdSKpSrM.NN9ElNDamu7qKnUna4LD6N.9Eo.g9GqSl48uID7w01VNKN1r2iyLJRCGg; TS01871345=016e3b076f34a422c5573c731ca66a2b7157c4810c035638d07a7c55ab6c5b01f8c44ddbbff9190f0c8d1faf43ea9e312d0188ccf2; BIGipServerpool_sistemaswebb3-listados_8443_WAF=1329145866.64288.0000; TS0171d45d=011d592ce10bf6b8c9ffa149856bab443308113a7e3693865a2b941bef076b43f52559b07e24e82e6865a53022f9417de9223839e1; rxvt=1738454227591|1738450153034; dtPC=33$252427213_234h-vBHFCEDJVFCUKCFSNJVCCSKBDUTGDOOOU-0e0; cf_clearance=F92v15zJ6X3nVP3SgT2BW4IAYmzg2wYmQOlLHPc1tfc-1738452471-1.2.1.1-9Ve.H5qGjYD20l0EUd5iAD_07xi331OH1sPkFpuGbYJvLhAaRKWb8IKMaLpNf5Zxu2mVu.eG4Oq6U76dARGR0uOSn8qvnliDinHSacGauGHdcAHO62NYKawJeaFt3ASY0pWOtUOz0nwz9_uENoGWaRfCGDO3P3mX6emNatoiOZvxyFiQEKtl8zvJVVoBEGotx3j2E9O9KHLDR4KztOV0nryeI0HWhSWDEV3_uWAZcCj96W.Nkv5Ph2hkvDKFj5WUwtXPyDHFN64YCA4qtXkp7z0jOuXXKhv.VfnIB0tN0hU',
                'priority': 'u=1, i',
                'referer': 'https://sistemaswebb3-listados.b3.com.br/',
                'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            },

            # Headers página 6
            'headers_6': {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'pt-BR,pt;q=0.6',
                # 'cookie': 'dtCookie=v_4_srv_33_sn_76EF270DB99B9F2DFDD25CE7443B193D_perc_100000_ol_0_mul_1_app-3Afd69ce40c52bd20e_1_rcs-3Acss_0; TS0134a800=016e3b076ff209bbc93f9b7db1f0d49be631132f17dfc874d374d43078a3e0ae6268ec31e405025baf7c325362897f0451fd0b23cd; rxVisitor=17384415824942VP8SUIC1F5NGU3S4LRAK2QHNAAB5LP6; dtSa=-; __cf_bm=meqy8ELt.6lJpw3qa6kU3F0sFaAZ9jYiM8ilvm1s.WY-1738451946-1.0.1.1-ZbDxqsIrBbMdGAzlqF.YKdSKpSrM.NN9ElNDamu7qKnUna4LD6N.9Eo.g9GqSl48uID7w01VNKN1r2iyLJRCGg; TS01871345=016e3b076f34a422c5573c731ca66a2b7157c4810c035638d07a7c55ab6c5b01f8c44ddbbff9190f0c8d1faf43ea9e312d0188ccf2; TS0171d45d=011d592ce10bf6b8c9ffa149856bab443308113a7e3693865a2b941bef076b43f52559b07e24e82e6865a53022f9417de9223839e1; BIGipServerpool_sistemaswebb3-listados_8443_WAF=1329140746.64288.0000; cf_clearance=INbMZX0bOFhveZC1kLK59LgavsMJzQMGomYwfbz4Eao-1738452543-1.2.1.1-Cs8SoacZUJ1oMb0bOOm026Z._Li5RCXB7e6dMgf9T3a3yq_tJNKh3eVBhl8f35qf5x2iiJ_FiHmZaf3IpNZjy2Qvn4Lt9Q.wywggX5TPHZwFFVXgyFadu7YeJbMlhuZrbC09fdU8qfZRVg._umHzd0Xy0wB4L78eGGDC9zti1gMo_joZC4KayGQ6wYaYw9rz7vnS43OCGSK_TVbmKpWJp3BQjDzuoO.w.CypT2F9Kmz1ZdST78jwh7IqpdhpzImXt.sQOvt4ujggZ9.ouqxxyBHCiDtUobXD.M9mb7u56Ng; rxvt=1738454299689|1738450153034; dtPC=33$252499333_186h-vBHFCEDJVFCUKCFSNJVCCSKBDUTGDOOOU-0e0',
                'priority': 'u=1, i',
                'referer': 'https://sistemaswebb3-listados.b3.com.br/',
                'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            },

            # Headers página 7
            'headers_7': {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'pt-BR,pt;q=0.6',
                # 'cookie': 'dtCookie=v_4_srv_33_sn_76EF270DB99B9F2DFDD25CE7443B193D_perc_100000_ol_0_mul_1_app-3Afd69ce40c52bd20e_1_rcs-3Acss_0; TS0134a800=016e3b076ff209bbc93f9b7db1f0d49be631132f17dfc874d374d43078a3e0ae6268ec31e405025baf7c325362897f0451fd0b23cd; rxVisitor=17384415824942VP8SUIC1F5NGU3S4LRAK2QHNAAB5LP6; dtSa=-; __cf_bm=meqy8ELt.6lJpw3qa6kU3F0sFaAZ9jYiM8ilvm1s.WY-1738451946-1.0.1.1-ZbDxqsIrBbMdGAzlqF.YKdSKpSrM.NN9ElNDamu7qKnUna4LD6N.9Eo.g9GqSl48uID7w01VNKN1r2iyLJRCGg; TS01871345=016e3b076f34a422c5573c731ca66a2b7157c4810c035638d07a7c55ab6c5b01f8c44ddbbff9190f0c8d1faf43ea9e312d0188ccf2; TS0171d45d=011d592ce10bf6b8c9ffa149856bab443308113a7e3693865a2b941bef076b43f52559b07e24e82e6865a53022f9417de9223839e1; BIGipServerpool_sistemaswebb3-listados_8443_WAF=1329140746.64288.0000; cf_clearance=cbLgmzjWkRLuKnE5PdAoEa9z9fRW1cVOXBxx62abwyY-1738452627-1.2.1.1-wdzQBzKUN7swJ6rqRR8FaLWXk4uGXc3fbkrjOAIL4XIIE05kkbiTDNQNWkHWDAHCRNjqXbF9prNKkDyr2_qsqdRuR9iocmWHC7OmFy7Qq351TvsdoGl27UQZMKfnmD4EQxR6dnfOPIIJfhW0nthG_dxkzRuvHg4PHsGtitJRj3.UKlK9BQxUxDRyKBOvy7tlIur_7B5GjYlw_R.1tgUY05hEERxkaRLkzSXadobSy3VTic2qmt9GOfw8gaIDOveQ1MVa6sx3KETwMPA7zQiuMn3egI0Bqh1GtsuoYoajmUE; rxvt=1738454383981|1738450153034; dtPC=33$252583550_476h-vBHFCEDJVFCUKCFSNJVCCSKBDUTGDOOOU-0e0',
                'priority': 'u=1, i',
                'referer': 'https://sistemaswebb3-listados.b3.com.br/',
                'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            }
        }

        # Dicionários das URLs
        dict_url = {
            # URL página 1
            'url_1': 'https://sistemaswebb3-listados.b3.com.br/stockProgramProxy/StockProgramCall/GetListedCompany/eyJrZXl3b3JkIjoiIiwiZGF0ZSI6IjIwMjUtMDEtMzEiLCJsYW5ndWFnZSI6InB0LWJyIiwicGFnZU51bWJlciI6MSwicGFnZVNpemUiOjIwfQ==',
            # URL página 2
            'url_2': 'https://sistemaswebb3-listados.b3.com.br/stockProgramProxy/StockProgramCall/GetListedCompany/eyJrZXl3b3JkIjoiIiwiZGF0ZSI6IjIwMjUtMDItMDEiLCJsYW5ndWFnZSI6InB0LWJyIiwicGFnZU51bWJlciI6MiwicGFnZVNpemUiOjIwfQ==',
            # URL página 3
            'url_3': 'https://sistemaswebb3-listados.b3.com.br/stockProgramProxy/StockProgramCall/GetListedCompany/eyJrZXl3b3JkIjoiIiwiZGF0ZSI6IjIwMjUtMDItMDEiLCJsYW5ndWFnZSI6InB0LWJyIiwicGFnZU51bWJlciI6MywicGFnZVNpemUiOjIwfQ==',
            # URL página 4
            'url_4': 'https://sistemaswebb3-listados.b3.com.br/stockProgramProxy/StockProgramCall/GetListedCompany/eyJrZXl3b3JkIjoiIiwiZGF0ZSI6IjIwMjUtMDItMDEiLCJsYW5ndWFnZSI6InB0LWJyIiwicGFnZU51bWJlciI6NCwicGFnZVNpemUiOjIwfQ==',
            # URL página 5
            'url_5': 'https://sistemaswebb3-listados.b3.com.br/stockProgramProxy/StockProgramCall/GetListedCompany/eyJrZXl3b3JkIjoiIiwiZGF0ZSI6IjIwMjUtMDItMDEiLCJsYW5ndWFnZSI6InB0LWJyIiwicGFnZU51bWJlciI6NSwicGFnZVNpemUiOjIwfQ==',
            # URL página 6
            'url_6': 'https://sistemaswebb3-listados.b3.com.br/stockProgramProxy/StockProgramCall/GetListedCompany/eyJrZXl3b3JkIjoiIiwiZGF0ZSI6IjIwMjUtMDItMDEiLCJsYW5ndWFnZSI6InB0LWJyIiwicGFnZU51bWJlciI6NiwicGFnZVNpemUiOjIwfQ==',
            # URL página 7
            'url_7': 'https://sistemaswebb3-listados.b3.com.br/stockProgramProxy/StockProgramCall/GetListedCompany/eyJrZXl3b3JkIjoiIiwiZGF0ZSI6IjIwMjUtMDItMDEiLCJsYW5ndWFnZSI6InB0LWJyIiwicGFnZU51bWJlciI6NywicGFnZVNpemUiOjIwfQ=='
        }

        # Lista JSON
        self.lst_buyback_json = []
    
        # Iterando em cada página da B3 fazendo a requisição GET para a URL da b3
        for cookie, header, url in zip(dict_cookies.items(), dict_headers.items(), dict_url.items()):
            response = requests.get(
                url=url[1],
                cookies=cookie[1],
                headers=header[1],
            )

            # Transformando em json
            buyback = response.json()
            self.lst_buyback_json.append(buyback)

    def process_data(self):
        # Lista dos buybacks
        lst_buyback = []

        # Iterando sobre a lista JSON
        for i in range(len(self.lst_buyback_json)):
            df_buyback_result = pd.DataFrame(self.lst_buyback_json[i]['results'])
            lst_buyback.append(df_buyback_result)

        # Concatenando todos os DataFrames da lista em um único DataFrame
        df_buyback_final = pd.concat(lst_buyback, ignore_index=True)

        # Trocando a string '/' por '-'
        df_buyback_final['aprrovedDate'] = df_buyback_final['aprrovedDate'].str.replace('/', '-')
        df_buyback_final['startDate'] = df_buyback_final['startDate'].str.replace('/', '-')
        df_buyback_final['endDate'] = df_buyback_final['endDate'].str.replace('/', '-')

        # A recompra da OI está com um erro na coluna 'endDate' ('31-12-9999') tenho que retirar do df p/ transformar em datetime
        df_buyback_final = df_buyback_final.query("endDate != '31-12-9999'")

        # Fazendo uma cópia do df
        df_buyback_final =  df_buyback_final.copy()

        # Transformando as colunas em datetime
        df_buyback_final['aprrovedDate'] = pd.to_datetime(df_buyback_final['aprrovedDate'], format='%d-%m-%Y')
        df_buyback_final['startDate'] = pd.to_datetime(df_buyback_final['startDate'], format='%d-%m-%Y')
        df_buyback_final['endDate'] = pd.to_datetime(df_buyback_final['endDate'], format='%d-%m-%Y')

        # Separando a coluna 'quantity' em duas novas colunas ('type_stock' e 'quantity_only') - (ex: '2.000.000 (ON)') -> ('2.000.000') e ('ON')
        df_buyback_final['type_stock'] = df_buyback_final['quantity'].str.extract(r"\((.*?)\)")
        df_buyback_final['quantity_only'] = df_buyback_final['quantity'].str.replace(r"\(.*?\)", "", regex=True)

        # Separando a coluna 'company' em duas novas colunas ('segment' e 'ticker') - (ex: 'VIVARA (NM)') -> ('VIVARA') e ('NM')
        df_buyback_final['segment'] = df_buyback_final['company'].str.extract(r"\((.*?)\)")
        df_buyback_final['ticker'] = df_buyback_final['company'].str.replace(r"\(.*?\)", "", regex=True)

        # Selecionando as principais colunas
        df_buyback_final = df_buyback_final[['startDate', 'endDate', 'ticker', 'quantity_only', 'segment', 'type_stock']]

        # Ordenando o df
        df_buyback_final = df_buyback_final.sort_values(by='startDate')

        # Transformando a coluna 'quantity_only' em int
        df_buyback_final['quantity_only'] = df_buyback_final['quantity_only'].str.replace('.', '').astype(int)

        # Data do dia em que ocorreu o scraping dessa tabela
        data_atual = datetime.date.today()
        data_atual_str = data_atual.strftime('%Y-%m-%d')
        data_atual_str = data_atual_str.replace('-', '_')

        # Transformando em um arquivo csv
        df_buyback_final.to_csv(f'C:/Users/vitor/projetos_python/python_b3/web-scraping/dados-financ-econ/buyback_b3/buyback_{data_atual_str}.csv', sep=';')


def main():
    buyback_b3 = buyback()
    buyback_b3.process_data()

if __name__ == "__main__":
    main()