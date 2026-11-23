using UnityEngine;

public class SentryGunSystem : Singleton<SentryGunSystem>
{
	private NameKeyPool pool;

	protected override void Awake()
	{
	}

	public static RecyclableObject Get(GameObject prefab)
	{
		return null;
	}
}
