using System;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu]
public class EffectAsset : ScriptableObject
{
	[Serializable]
	public struct EffectData
	{
		public string name;

		public GameObject[] effects;
	}

	[SerializeField]
	private List<EffectData> asset;

	public GameObject GetPrefab(string name, int index = -1)
	{
		return null;
	}
}
