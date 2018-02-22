using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[ExecuteInEditMode]
public class CarDetec : MonoBehaviour {
	public Material mat;
	// Use this for initialization
	void onRenderImage (RenderTexture src, RenderTexture dest) {
		
		Graphics.Blit(src, dest, mat);
	}
	
	
}
