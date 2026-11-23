using System;
using UnityEngine;

[Serializable]
public struct KnifeAttackData
{
	public float damage;

	public float range;

	public float angle;

	public bool hitStun;

	public int damageTag;

	public GameObject decal;

	public string decalSndName;
}
