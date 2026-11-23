using System;
using UnityEngine;

[Serializable]
public struct MissileData
{
	public int clip;

	public int ammo;

	public GameObject prefab;

	public float damage;

	public float range;

	public float damageFactorByDistance;

	public float velocity;

	public float extraGravity;

	public float throwAngle;

	public float expTime;

	public bool ignoreWall;
}
