using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarGenerator : MonoBehaviour {

	public CarTemplate oneCar;
	
	void Awake(){
		
		string loadeditem = ReadJson.LoadJsonAsResource("DataForSettings/VehicleData/cars");
		Debug.Log(loadeditem);
		oneCar = JsonUtility.FromJson<CarTemplate>(loadeditem);
	}

	// Use this for initialization
	
	void Start () {
		/*for (int y = 0; y < 5; y++) {
		    for (int x = 0; x < 5; x++) {
		        Instantiate(brick, new Vector3(x, y, 0), Quaternion.identity);
		    }
		}
		*/
	}
	
	
}
