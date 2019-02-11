# -*- coding: utf-8 -*-
import ast
import json
import boto3
import os

##########
# バゲットの名前
bucket_name = os.environ['S3_BUCKET']

##########
# S3にアップロード（高LV API）
def put_s3(w_dict):
    try:
        ##########        
        # AWSサービスの設定
        s3 = boto3.resource('s3')
        
        ##########
        # KEYの名前
        # 年月
        # 　└─　社員番号
        # 　　　　├─　IN
        # 　　　　│　　└─　KEY(YYYYMMDDHHMMSS)
        # 　　　　├─　OUT
        # 　　　　│　　└─　KEY(YYYYMMDDHHMMSS)
        # 　　　　└─　TOTAL
        # 　　　　　　　└─　KEY(YYYYMMDDHHMMSS)
        key_name = w_dict['Key_name'][0:6] + '/' + w_dict['No'] + '/' + w_dict['Status'] + '/' + w_dict['Key_name']

        ##########
        # 辞書型から文字列に変換
        body_data = str(w_dict)
        
        ##########
        # オブジェクトのFULL_PATH設定
        obj_path = s3.Object(bucket_name, key_name)

        ##########
        # ファイルアップ
        response = obj_path.put(Body=body_data)
    except:
        print("*** put_s3:ERR ***")


##########
# S3からダウンロード（高LV API）
def get_s3(w_dict):
    try:
        ##########
        # AWSサービスの設定
        s3 = boto3.resource('s3')

        ##########
        # バゲットの情報取得
        bucket = s3.Bucket(bucket_name)
        
        ##########
        # バゲットにあるKEYを取得
        key_list = []
        for obj_summary in bucket.objects.filter(Prefix=w_dict['Key_name'][0:6]+'/'+w_dict['No']+"/IN/"):
            key_list.append(obj_summary.key)

        ##########
        # バゲットリストを逆ソート（降順）
        key_list.sort(reverse=True)

        ##########
        # 最新のKEYを選択
        key_name = key_list[0]
        
        ##########
        # KEYの情報取得
        obj = s3.Object(bucket_name, key_name)

        ##########
        # KEYの情報取得
        response = obj.get()
        b_body = response['Body'].read()

        ##########
        # バイトから文字列へ変換
        s_body = b_body.decode('utf-8')
        
        ##########
        # 文字列から辞書型へ変換
        rtn_dict = ast.literal_eval(s_body)
        
        ##########
        # return
        return rtn_dict
    except:
        print("*** get_s3:ERR ***")




##########
# S3からダウンロード（高LV API）
def get_s3_all(w_dict):
    try:
        ##########
        # AWSサービスの設定
        s3 = boto3.resource('s3')
        
        ##########
        # バゲットの情報取得
        bucket = s3.Bucket(bucket_name)
        
        ##########
        # バゲットにあるKEYを取得
        key_list = []
        for obj_summary in bucket.objects.filter(Prefix=w_dict['Key_name'][0:6]+'/'+w_dict['No']+"/OUT/"):
            key_list.append(obj_summary.key)
            
        ##########
        # バゲットリストをソート（昇順）
        key_list.sort()
        
        ##########
        # 読み込み結果のリストを初期化
        # リストに辞書を登録する
        dict_list = []
        
        ##########
        # 全てのKEYを取得
        for key_name in key_list:
            
            ##########
            # KEYの情報取得
            obj = s3.Object(bucket_name, key_name)
            
            ##########
            # KEYの情報取得
            response = obj.get()
            b_body = response['Body'].read()
            
            ##########
            # バイトから文字列へ変換
            s_body = b_body.decode('utf-8')
            
            ##########
            # 文字列から辞書型へ変換
            rtn_dict = ast.literal_eval(s_body)
            
            ##########
            # リストに追加
            dict_list.append(rtn_dict)
            
        ##########
        # リスト化された辞書をreturn
        return dict_list
        
    except:
        print("*** get_s3_all:ERR ***")