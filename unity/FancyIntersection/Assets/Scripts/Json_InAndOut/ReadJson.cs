using System.Collections;
using System.Collections.Generic;
using UnityEngine;



public class ReadJson : MonoBehaviour{

	public static string LoadJsonAsResource(string filepath){
		//string purefilepath = filepath.Replace(".json", "");
	
		TextAsset loadedJsonFile = Resources.Load<TextAsset>(filepath);
		return loadedJsonFile.text;
		
		string JsonString = Resources.Load(filepath, typeof(TextAsset)).ToString();


		/*
		filepath = Path.Combine(Application.streamingAssetsPath, filepath);
		if (File.Exists(filepath)){
			string data = File.ReadAllText(filepath);
			CarTemplate oneCar = JsonUtility.FromJson<CarTemplate> (data);

			data = 
		}
		*/


	}// public static string LoadJsonAsResource(string filepath)

	public string url = "http://images.earthcam.com/ec_metros/ourcams/fridays.jpg";
    void Start () {
		 string url = "http://images.earthcam.com/ec_metros/ourcams/fridays.jpg";
         WWW www = new WWW(url);
         StartCoroutine(WaitForRequest(www));
     }
    IEnumerator WaitForRequest(WWW www)
    {
        
        yield return www;
        
        // check for errors
		if (www.error == null)
		{
			Debug.Log("WWW Ok!: " + www.text);
			
		} else {
		 Debug.Log("WWW Error: "+ www.error);
		}    
    }
}
