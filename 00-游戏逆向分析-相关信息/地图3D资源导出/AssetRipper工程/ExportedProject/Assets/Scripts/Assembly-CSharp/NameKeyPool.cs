using System.Collections;
using UnityEngine;

public class NameKeyPool : ObjectPool
{
	private Hashtable hashtable;

	public NameKeyPool(Transform container)
		: base(null)
	{
	}

	public override void Recycle(RecyclableObject obj)
	{
	}

	public RecyclableObject Get(GameObject prefab)
	{
		return null;
	}

	public RecyclableObject Get(string name)
	{
		return null;
	}
}
