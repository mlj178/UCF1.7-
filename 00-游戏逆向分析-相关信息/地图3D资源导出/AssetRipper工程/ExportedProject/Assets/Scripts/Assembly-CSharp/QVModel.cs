using System;
using UnityEngine;

public class QVModel : Model
{
	[Serializable]
	public struct Data
	{
		public Transform Model;

		public Vector3 Pos_OnHand;

		public Vector3 Euler_OnHand;

		public Vector3 Pos_GiveUp;

		public Vector3 Euler_GiveUp;

		public ParticleSystem GunFire;
	}

	public Rigidbody rigidBody;

	[SerializeField]
	private Data left;

	[SerializeField]
	private Data right;

	[SerializeField]
	public float giveUpScale;

	private Weapon bindWpn;

	[SerializeField]
	private Transform pickUpArea;

	private float startCheckPickUpTime;

	private static readonly Vector3 giveUpScale_3rd;

	public bool isDropState => false;

	public bool isMapGun { get; private set; }

	public void SetOnCharacter(CharacterModel character)
	{
	}

	public void GiveUp(Weapon weapon, Vector3 pos, Quaternion rotation, float speed)
	{
	}

	public override void TryRecycle(bool roundRecycle)
	{
	}

	public override void Recycle(bool roundRecycle)
	{
	}

	private void RecycleModel()
	{
	}

	public void SetVisible(bool visible)
	{
	}

	public void SetGunFireState(bool leftHand, bool state)
	{
	}

	public void StopGunFire()
	{
	}

	public void SetOnMap(Transform setPos, Vector3 localPos, Vector3 localEuler)
	{
	}

	private void OnTriggerStay(Collider other)
	{
	}
}
