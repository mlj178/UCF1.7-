using UnityEngine;

public abstract class ObjectPool
{
	public Transform container { get; private set; }

	public ObjectPool(Transform container)
	{
	}

	public abstract void Recycle(RecyclableObject obj);
}
