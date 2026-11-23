using UnityEngine;
using UnityEngine.UI;

public class HUD_Nano6Gauge : SimpleHudBase
{
	private bool humanType;

	[SerializeField]
	private Image headImage;

	[SerializeField]
	private Image backgroundImage;

	[SerializeField]
	private Image duration;

	[SerializeField]
	private Sprite[] asset;

	[SerializeField]
	private RectTransform delta;

	private float deltaHideTime;

	protected override void Awake()
	{
	}

	protected override void MyPlayerInit(Player myPlayer)
	{
	}

	private void OnNanoExpChange(int arg1, int newExp)
	{
	}

	private void OnSoldierExpChange(float oldExp, float newExp)
	{
	}

	private void OnTeamChange(Team team)
	{
	}

	public void SetType(bool isHuman)
	{
	}

	private void Update()
	{
	}

	public void SetFillAmount(float currentExp, int[] needExp)
	{
	}

	public void ShowDelta()
	{
	}
}
