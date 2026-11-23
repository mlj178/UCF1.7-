using System;
using UnityEngine;

[Serializable]
public struct ZoomAction
{
	[Serializable]
	public struct ZoomData
	{
		public int type;

		public float fovScale;

		public Sprite sprite;
	}

	public float openTime;

	public float closeTime;

	public ZoomData[] datas;

	public bool closeZoomWhenShoot;
}
