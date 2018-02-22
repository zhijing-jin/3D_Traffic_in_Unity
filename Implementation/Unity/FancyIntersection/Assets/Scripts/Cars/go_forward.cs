using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class go_forward : MonoBehaviour {

	public float moveSpeed = 10f;
    public float turnSpeed = 50f;

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	
    
    
    void Update ()
    {
        transform.Translate(Vector3.forward * moveSpeed * Time.deltaTime);
        
        
    }
}
