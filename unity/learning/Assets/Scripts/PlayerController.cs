using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerController : MonoBehaviour {

	private Rigidbody rb;

	public float speed = 100;
	// Use this for initialization
	void Start(){
		
		rb = GetComponent<Rigidbody>();

	}

	void FixedUpdate () {
		float moveHori = Input.GetAxis("Horizontal");
		float moveVerti = Input.GetAxis("Vertical");
		
		Vector3 movement = new Vector3 (moveHori, 0.0f, moveVerti);

		rb.AddForce(movement * speed);


	}
	
	
}
