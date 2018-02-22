using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.IO;

public class DesignedMovement : MonoBehaviour {
	public CarTemplate CarData;
	WWW www;
	public string url; // localhost that Flask post json onto
	WebRequest request; 

	WebResponse response;
	StreamReader reader;

	void Start () {
		 
         www = new WWW(url);
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
	
	
	
	// Update is called once per frame
	void Update () {
		/*
		string loadeditem = ReadJson.LoadJsonAsResource("DataForSettings/VehicleData/cars_realtime_updates");
		*/
		request = WebRequest.Create (url);
		request.ContentType = "application/json; charset=utf-8";
		response = request.GetResponse ();
		Stream dataStream = response.GetResponseStream ();  
		reader = new StreamReader (dataStream); 
		string loadeditem = reader.ReadToEnd ();  






		// string loadeditem = www.text;
		Debug.Log("loaded item:"+loadeditem);
		CarData = JsonUtility.FromJson<CarTemplate>(loadeditem);
		Vector3 movement = CarData.movement;
		transform.rotation = Quaternion.LookRotation(movement);
		transform.position = CarData.position;
		reader.Close();
		response.Close();
		
		
	}

}
