using System;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu]
public class WeaponAsset : ScriptableObject
{
	[NonSerialized]
	public bool loaded;

	public List<GameObject> weaponList;

	public GameObject GetWeaponPrefab(int index)
	{
		return null;
	}
}
