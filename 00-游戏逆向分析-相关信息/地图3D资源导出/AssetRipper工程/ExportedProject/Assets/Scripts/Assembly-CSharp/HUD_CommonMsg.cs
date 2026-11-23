using UnityEngine;
using UnityEngine.UI;

public class HUD_CommonMsg : Singleton<HUD_CommonMsg>
{
	[SerializeField]
	private GameObject msgBox;

	[SerializeField]
	private Text msgText;

	private float msgBoxHideTime;

	[SerializeField]
	private RectTransform triggerTipRect;

	[SerializeField]
	private Image triggerTip;

	[SerializeField]
	private CommonHud_1 modeTipText;

	[SerializeField]
	private HUD_Gauge settingGauge;

	private CommonHud_1 wpnModeTip_RepeatFire;

	private CommonHud_1 wpnModeTip_GrenadeGun;

	private float mouseSpeedStartContinuousAdjustTime;

	protected override void Awake()
	{
	}

	private void Start()
	{
	}

	private void ShowModeTipText()
	{
	}

	private void Update()
	{
	}

	public static void ShowMsgBox(string msg, float showTime = 2f, bool cancelSameMsgSnd = true)
	{
	}

	public static void SetTriggerTip(Sprite sprite)
	{
	}

	private bool MouseSpeedAdjust()
	{
		return false;
	}

	public void ShowTip_GrenadeGunMode(bool isOpen)
	{
	}

	public void ShowTip_RepeatFireMode(bool isOpen)
	{
	}
}
