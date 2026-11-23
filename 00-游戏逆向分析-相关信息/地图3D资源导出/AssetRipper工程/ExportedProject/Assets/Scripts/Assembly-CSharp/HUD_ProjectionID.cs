using UnityEngine;

public class HUD_ProjectionID : Singleton<HUD_ProjectionID>
{
	public RectTransform canvasRect;

	[SerializeField]
	private HUD_KillerSign killerSign;

	[SerializeField]
	private GameObject supplyBoxPrefab;

	private NameKeyPool pool;

	protected override void Awake()
	{
	}

	public static void SetKiller(Transform killer)
	{
	}

	public static void AddSupplyBox(SupplyBox supplyBox)
	{
	}

	public static RecyclableObject GetSign(GameObject prefab)
	{
		return null;
	}
}
