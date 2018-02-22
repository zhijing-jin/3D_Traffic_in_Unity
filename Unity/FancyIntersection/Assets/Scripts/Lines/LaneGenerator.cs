using System.Collections;
using System.Collections.Generic; //for transform function, List<>
using UnityEngine;
using System.Net;
using System.IO;


[System.Serializable]
public class LineContainer{
	public List<LineTemplate> LineList = new List<LineTemplate>();
}


public class LaneGenerator : MonoBehaviour {

	// private GameObject Lines; // for assigning "parent"
	public LineContainer oneLineCon;
	public GameObject LinePrefab;
	WWW www;
	public string url; // localhost that Flask post json onto
	
	WebRequest request; 

	WebResponse response;
	StreamReader reader;

	void Awake(){
		
		// string loadeditem = ReadJson.LoadJsonAsResource("DataForSettings/RoadData/lanes");
		// Debug.Log(loadeditem);	
		www = new WWW(url);
        StartCoroutine(WaitForRequest(www));

        
		request = WebRequest.Create (url);
		request.ContentType = "application/json; charset=utf-8";
		response = request.GetResponse ();
		Stream dataStream = response.GetResponseStream ();  
		reader = new StreamReader (dataStream); 
		string loadeditem = reader.ReadToEnd ();  
		// string loadeditem = www.text;
		Debug.Log("loaded item:"+loadeditem);
		




		oneLineCon = JsonUtility.FromJson<LineContainer>(loadeditem);
		
		foreach ( LineTemplate lineSegment in oneLineCon.LineList){
			DrawLine(lineSegment);
		}

		
	}

	void DrawLine(LineTemplate lineSegment){
		GameObject one_line = Instantiate(LinePrefab);
		one_line.transform.position = lineSegment.position;
		one_line.transform.localScale = lineSegment.scale;
		one_line.transform.Rotate(lineSegment.rotation);
		// Color color = Color.red;
		// color.a = 255;
		// one_line.GetComponent<Renderer>().material.color = color;
		one_line.transform.parent = GameObject.Find("Lines").transform;
		
		//one_line.lineInformation = lineSegment;


	}//DrawLine()
	

	


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
