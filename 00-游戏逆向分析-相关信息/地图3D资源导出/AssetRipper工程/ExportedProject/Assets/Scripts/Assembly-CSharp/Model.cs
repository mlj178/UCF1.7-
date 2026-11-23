using System;
using System.Collections.Generic;
using UnityEngine;

public class Model : RecyclableObject
{
	public enum Type
	{
		Character = 0,
		PlayerView = 1
	}

	[Serializable]
	public struct Socket
	{
		public string name;

		public Transform node;

		public Vector3 offset;

		public Vector3 euler;
	}

	public List<GameObject> objectInPV;

	public List<GameObject> objectInCV;

	public List<Socket> sockets;

	public Player owner { get; protected set; }

	public bool isActive => false;

	public virtual void SetOwner(Player newOwner)
	{
	}

	protected virtual void SetValidOwner()
	{
	}

	protected virtual void SetNullOwner()
	{
	}

	protected virtual void RemoveFromOldOwner()
	{
	}

	private void OnOwnerObserveModeChange(Type mode)
	{
	}

	public void SetModelLayer(Type mdlType, int layer)
	{
	}

	public override void Recycle(bool roundRecycle)
	{
	}

	public void BindSocket(Transform tsf, string socketName)
	{
	}

	public void BindSocket(Transform tsf, string socketName, Vector3 offset, Vector3 euler)
	{
	}

	public void BindSocketInWorldSpace(Transform tsf, string socketName, Vector3 offset, Vector3 euler)
	{
	}
}
