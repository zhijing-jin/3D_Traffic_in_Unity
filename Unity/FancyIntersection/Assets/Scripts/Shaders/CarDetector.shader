﻿Shader "Custom/CarDetector"
{
	Properties
	{
		_MainTex ("Main Texture", 2D) = "white" {}
	}
	SubShader
	{
		// No culling or depth
		Cull Off ZWrite Off ZTest Always

		Pass
		{
			CGPROGRAM
			#pragma vertex vert
			#pragma fragment frag
			
			#include "UnityCG.cginc"

			struct appdata
			{
				float4 vertex : POSITION;
				float2 uv : TEXCOORD0;
			};

			struct v2f
			{
				float2 uv : TEXCOORD0;
				float4 vertex : SV_POSITION;
			};

			v2f vert (appdata v)
			{
				v2f o;
				o.vertex = UnityObjectToClipPos(v.vertex);
				o.uv = v.uv;
				return o;
			}
			
			sampler2D _MainTex;

			fixed4 frag (v2f i) : SV_Target
			{
				fixed4 col = tex2D(_MainTex, i.uv);
				// fixed4 col = tex2D(_MainTex, i.uv + float2(0, 0.1));
				// fixed4 col = tex2D(_MainTex, i.uv + float2(0, IN.vertex.x/5000 + _time[0]));

				// just invert the colors
				col = 1 - col;
				col.r = 1;
				return col;
			}
			ENDCG
		}
	}
}
