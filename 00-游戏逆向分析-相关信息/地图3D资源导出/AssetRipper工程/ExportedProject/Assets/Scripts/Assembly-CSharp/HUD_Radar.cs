using UnityEngine;

public class HUD_Radar : Singleton<HUD_Radar>
{
	[SerializeField]
	private RectTransform mask;

	[SerializeField]
	private RectTransform minimap;

	[SerializeField]
	private RectTransform frame;

	[SerializeField]
	private RectTransform iconsContainer;

	[SerializeField]
	private GameObject simpleRadarIconPrefab;

	[SerializeField]
	private GameObject entityRadarIconPrefab;

	[SerializeField]
	private GameObject supplyBoxIconPrefab;

	private NameKeyPool radarIconPool1;

	private NameKeyPool radarIconPool2;

	public static bool hideEnemy;

	public static float scale;

	public static float pixelPerDistance => 0f;

	public static Vector3 originalPos => default;

	protected override void Awake()
	{
	}

	private void Start()
	{
	}

	private void OnNewPlayerJoin(Player player)
	{
	}

	private void Update()
	{
	}

	public static RectTransform GetIconContainer()
	{
		return null;
	}

	public static HUD_RadarIcon AddIcon(Transform bind, bool addInMask = false)
	{
		return null;
	}

	public static void AddEntity(Entity entity)
	{
	}

	public static void AddSupplyBox(SupplyBox supplyBox)
	{
	}

	public static HUD_RadarIcon GetIcon(GameObject prefab, bool addInMask)
	{
		return null;
	}
}
