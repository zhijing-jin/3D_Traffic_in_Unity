using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class LineDrawer : MonoBehaviour {

	private GameObject Lines; // for assigning "parent"
	public GameObject LinePrefab; // and manually "drag" your needed prefab in the interface.

	
	// Use this for initialization
	void Start () {
		// FOR A CUBE		
		GameObject one_lane = Instantiate(LinePrefab); // GameObject one_lane = GameObject.CreatePrimitive(PrimitiveType.Cube);
		

		one_lane.name = "one_lane";
		one_lane.GetComponent<Renderer>().material.color = new Color(139f/255f, 69f/255f, 19f/255f, 1f);
		
        one_lane.transform.position = new Vector3(0, 0.5F, 0);
        one_lane.transform.localScale = new Vector3(1,2,10);
		// GameObjectUtility.SetParentAndAlign(one_lane)
        one_lane.transform.parent = GameObject.Find("Lines").transform; // make the parent // GameObjectUtility.SetParentAndAlign(one_lane)
        



		//FOR A LINE RENDERER
		GameObject lineObj = new GameObject("NewLine", typeof(LineRenderer));
		LineRenderer line = lineObj.GetComponent<LineRenderer>();
		line.startWidth = 1f;
		line.endWidth = 1f;
		line.startColor = Color.white;
		line.endColor = Color.white;
		line.SetPosition(0, Vector3.zero);
		line.SetPosition(1, Vector3.forward);
		Material whiteDiffuseMat = new Material(Shader.Find("Unlit/Texture"));
		line.material = whiteDiffuseMat;
		/* texture */
		/*
		// Assigns a material named "Assets/Resources/DEV_Orange" to the object.
		Material newMat = Resources.Load("Materials/Roadline", typeof(Material)) as Material;
		lineObj.renderer.material = newMat;
		*/
	}
	
	// Update is called once per frame
	void Update () {
		
	}
}

/*
void DrawLine(Vector3 start, Vector3 end, Color color, float duration = 0.2f)
         {
             GameObject myLine = new GameObject();
             myLine.transform.position = start;
             myLine.AddComponent<LineRenderer>();
             LineRenderer lr = myLine.GetComponent<LineRenderer>();
             lr.material = new Material(Shader.Find("Particles/Alpha Blended Premultiply"));
             lr.SetColors(color, color);
             lr.SetWidth(0.1f, 0.1f);
             lr.SetPosition(0, start);
             lr.SetPosition(1, end);
             GameObject.Destroy(myLine, duration);
         }
*/