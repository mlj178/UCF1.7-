using UnityEngine;
using UnityEngine.UI;

public class HUD_Nano_FinalBattle : MonoBehaviour
{
	[SerializeField]
	private bool shakeIcon;

	[SerializeField]
	private RectTransform heroIconRect;

	[SerializeField]
	private RectTransform nanoIconRect;

	[SerializeField]
	private Text heroNumText;

	[SerializeField]
	private Text nanoNumText;

	[SerializeField]
	private Font normalFont;

	[SerializeField]
	private Font flashFont;

	private Vector2Int curCount;

	private Vector2 flashEndTime;

	[SerializeField]
	private AudioClip nanoCountDownSnd;

	private float nextKillNanoSndTime;

	private static readonly Vector2 heroIconPos;

	private static readonly Vector2 nanoIconPos;

	private void Awake()
	{
	}

	private void Update()
	{
	}

	public void SetActive(bool active)
	{
	}

	private void SetHeroCount(int count)
	{
	}

	private void SetNanoCount(int count)
	{
	}

	private void DeathEvent(DeathEventData evtData)
	{
	}

	private void ShakeIcon(RectTransform target, Vector2 originPos)
	{
	}
}
