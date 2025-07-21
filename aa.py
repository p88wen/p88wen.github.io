import os 
import sys 
import time 
import json 
import requests 
import re 
import random 
import hashlib 
import urllib.parse  
from datetime import datetime 
import zipfile 
from concurrent.futures  import ThreadPoolExecutor 
from tkinter import Tk, ttk, filedialog, messagebox, Toplevel 
 
class Spider: 
    def writeFile(self, path, content): 
        with open(path, 'wb') as f: 
            f.write(content)  
 
    def process_apk_info(self):
        final_output = [{"name":"推荐","list":[{"name":"影视更新","url":"","icon":"https://p88wen.github.io/fongmi.png","version":"NEW"}]}]  # 最终结果容器 
        config = ["fongmi", "okjack"]
        for own in config:
            url = f'https://github.com/FongMi/Release/tree-commit-info/{own}/apk/release' 
            headers = {
                "Content-Type": "application/json;charset=UTF-8",
                "github-verified-fetch": "true",
                "x-requested-with": "XMLHttpRequest"
            }
            try:
                response = requests.get(url,  headers=headers)
                response.raise_for_status() 
                data = response.json() 
                
                # 初始化当前维护者的数据容器 
                apk_list = []

                for apk_name, details in data.items(): 
                    if ".apk" in apk_name:
                        # 提取基础信息 
                        apk_name_part = apk_name.split('_',  1)[0]  if '_' in apk_name else apk_name 
                        
                        # 正则匹配架构和后缀
                        abi = re.search(r'-(\w+)_',  apk_name).group(1) if re.search(r'-(\w+)_',  apk_name) else None 
                        suffix = re.search(r'_([^-.]+)\.apk$',  apk_name).group(1) if re.search(r'_([^-.]+)\.apk$',  apk_name) else None 
                        
                        # 日期处理 
                        date_obj = datetime.fromisoformat(details["date"]) 
                        formatted_date = date_obj.strftime("%Y-%m-%d") 
                        
                        # 版本号提取 
                        #version_match = re.search(r'title="Update to (\d+\.\d+\.\d+)"', details["shortMessageHtmlLink"])
                        #version = version_match.group(1)  if version_match else None 
                        title_match = re.search(r'title="([^"]+)"',  details["shortMessageHtmlLink"]) 
                        version = title_match.group(1).replace("Update to ", "") if title_match else None 
                        #downloadurl = f'https://gh-proxy.com/raw.githubusercontent.com/FongMi/Release/refs/heads/{own}/apk/release/{apk_name}'
                        downloadurl = f'https://p88wen.github.io/{own}/apk/release/{apk_name}'               
                        # 构建APK信息对象 
                        apk_info = {
                            "name": apk_name_part,
                            "url":downloadurl,
                            "icon":'https://p88wen.github.io/fongmi.png',
                            "version": f"{suffix}-{version}" if suffix and version else ''
                        }
                        apk_list.append(apk_info) 
                
                # 将当前维护者数据添加到最终结果 
                final_output.append({ 
                    "name": own,
                    "list": apk_list 
                }) 
            except requests.RequestException as e: 
                print(f"请求错误: {e}") 
            except ValueError as e: 
                print(f"JSON解析错误: {e}") 
 
        # 将字符串转换为字节类型 
        self.writeFile("share/apk.json",  json.dumps(final_output,  ensure_ascii=False).encode('utf-8')) 
        return final_output 
 
 
if __name__ == '__main__': 
    spi = Spider() 
    init_result = spi.process_apk_info()  
    print(f"init_result运行完成:{init_result}") 
    print("全部运行完成，输入任意键退出") 
