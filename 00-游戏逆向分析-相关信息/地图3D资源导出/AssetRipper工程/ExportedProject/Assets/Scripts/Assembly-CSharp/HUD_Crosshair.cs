using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class HUD_Crosshair : Singleton<HUD_Crosshair>
{
	public enum Type
	{
		Common = 0,
		FalCamo = 1
	}

	[SerializeField]
	private RectTransform sniperCross;

	[SerializeField]
	private Image sniperCrossBackGround;

	[SerializeField]
	private RectTransform hitRect;

	private static float nextHitAnimAllowedTime;

	private static bool hideCrosshair;

	private Player player;

	[SerializeField]
	private GameObject[] allCrosshair;

	[SerializeField]
	private RectTransform crosshair1_horizontal;

	[SerializeField]
	private RectTransform crosshair1_vertical;

	private Type curCrosshairType;

	[SerializeField]
	private Text[] zoomTargetTexts;

	private List<RaycastHit> zoomRaycastTemp;

	private static readonly Color color_ZoomTeammate;

	private static readonly Color color_ZoomEnemy;

	protected override void Awake()
	{
	}

	private void Start()
	{
	}

	private void Update()
	{
	}

	private void ZoomTargetNameUpdate()
	{
	}

	protected override void OnDestroy()
	{
	}

	public void SetSniperCrossVisible(bool visible)
	{
	}

	public void DamageEvent(ref DamageEventData eventData)
	{
	}

	private void FocusPlayerChangeEvent(Player oldPlayer, Player newPlayer)
	{
	}

	public void CheckSniperZoomImage()
	{
	}

	public void SetType(Type crosshairType)
	{
	}
}
