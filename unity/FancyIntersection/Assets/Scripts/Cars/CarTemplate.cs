using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class CarTemplate {

	
	public Vector3 scale;
	public Vector3 position;
	public Vector3 rotation;
	public Vector3 movement;
	public float speed;
	public string somewords;

	public Vector3 getScale(){ return scale; }
	public Vector3 getPosition(){ return position; }
	public float getSpeed(){ return speed; }
}
