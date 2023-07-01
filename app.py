from flask import Flask,request,render_template,redirect,send_file
from urllib.parse import urljoin
#from flask import jsonify
import bs4,requests,uuid,os,shutil
from io import BytesIO
from zipfile import ZipFile
from glob import glob
app=Flask(__name__)
con,infor,total,imgCon,tog='','','','',''
@app.route('/',methods=['GET',"POST"])
def index():
    global con,imgCon,infor
    '''if(request.method=='POST'):
        con=request.form['urls']
        print(con)
        if con.strip():
            return render_template('download.html')
        else:
            return render_template('home.html',e='Enter a valid url') 
        '''
    return render_template('home.html',e='',infor=infor)

def scrape(con):
    res=''
    try:
        if con:
            res=requests.get(con)
            soup=bs4.BeautifulSoup(res.content,'lxml')
            images=soup.find_all('img')
            links=[]
            for i in images:
                src=i['src']
                links.append(urljoin(con,src))
            if not links:return False,links
            return True,links
        else:return False,[]
    except:
        return False,[] 
@app.route('/down',methods=['GET','POST'])
def down():
    global infor
    global total
    global con
    global tog
    links=[]
    print(request.method)
    if request.method=='POST':
        print("fsfsfs")
        con=request.get_json()['data']
        flag,links=scrape(con)
        total=len(links)
        check=os.listdir(os.getcwd())
        if 'send' in check: 
            shutil.rmtree('send', ignore_errors=True)
        os.mkdir('send')
        target = 'send'
        if links:
            for i in links:
                res=requests.get(i).content
                try:
                    f=open(f'send/{uuid.uuid1()}.{i[-3:]}','wb')
                    f.write(res)
                    f.close()
                except:pass
            stream = BytesIO()
            with ZipFile(stream, 'w') as zf:
                for file in glob(os.path.join(target,'*')):
                    zf.write(file, os.path.basename(file))
            stream.seek(0)
            return send_file(
                    stream,
                    as_attachment=True,
                    download_name='Images.zip',
                    mimetype='application/zip'
                        )

        else:
            stream=BytesIO()
            stream.write('There is no images in the given url'.encode())
            stream.seek(0)
            return send_file(stream,as_attachment=True,download_name='No-Images.txt',mimetype='application/text')
                    
            #otp=Response(stream, mimetype='application/zip', headers={'Content-Disposition': 'attachment;filename=Images.zip'})
            #return redirect('/')
    '''if not con.strip():
        infor='Please enter a valid url'
    elif not links:
        infor='Please enter a valid url'
    return render_template('home.html')
    '''
app.run(debug=True)