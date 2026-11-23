using System;
using UnityEngine;

[CreateAssetMenu]
public class SO_FxGroup : ScriptableObject
{
	[Serializable]
	public struct FxData
	{
		public GameObject fxPrefab;

		public float fxSize;

		public string attachName;

		public Vector3 offset;

		public Vector3 euler;
	}

	[Serializable]
	public enum AttachType
	{
		NodeAttach = 0,
		PlayerView = 1,
		PlayerSpace = 2
	}

	[SerializeField]
	private AttachType attachType;

	[SerializeField]
	private bool setNodeAsParent;

	public FxData[] allFx;

	public void Play(Model mdl)
	{
	}
}
