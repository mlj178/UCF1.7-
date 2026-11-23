using UnityEngine;

public class EffectManager : Singleton<EffectManager>
{
	[SerializeField]
	private GameObject recyclableImpulse;

	[SerializeField]
	private EffectAsset asset;

	private NameKeyPool effectPool;

	private SimpleObjectPool impulsePool;

	protected override void Awake()
	{
	}

	public static RecyclableObject PlayWorldEffect(string name, int index, Vector3 position, Quaternion rotation, bool autoActive = true)
	{
		return null;
	}

	public static RecyclableObject PlayWorldEffect(GameObject prefab, Vector3 position, Quaternion rotation, bool autoActive = true)
	{
		return null;
	}

	public static RecyclableObject PlayWorldEffect(GameObject prefab, Player player, bool autoActive = true)
	{
		return null;
	}

	public static RecyclableObject PlayAttachEffect(GameObject prefab, Transform parent, bool autoActive = true)
	{
		return null;
	}

	public static RecyclableObject GetEffect(GameObject prefab)
	{
		return null;
	}

	public static GameObject GetEffectPrefab(string name, int index = -1)
	{
		return null;
	}

	public static void CreateBulletHole(RaycastHit hitInfo)
	{
	}

	public static void PlayImpulse(Vector3 worldPos, float power, float minRadius, float maxRadius, float duration)
	{
	}
}
