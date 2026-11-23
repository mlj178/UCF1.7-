using System.Collections.Generic;
using UnityEngine;

public class SimpleObjectPool : ObjectPool
{
	private GameObject prefab;

	private Queue<RecyclableObject> pool;

	public SimpleObjectPool(GameObject prefab, Transform container)
		: base(null)
	{
	}

	public override void Recycle(RecyclableObject obj)
	{
	}

	public RecyclableObject Get()
	{
		return null;
	}
}
