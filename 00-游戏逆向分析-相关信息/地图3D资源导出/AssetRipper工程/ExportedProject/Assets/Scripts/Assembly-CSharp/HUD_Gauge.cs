using UnityEngine;
using UnityEngine.UI;

public class HUD_Gauge : MonoBehaviour
{
	protected float startTime;

	protected float totalTime;

	protected float hideTime;

	protected float curProgress;

	[SerializeField]
	private RectTransform progressRect;

	[SerializeField]
	private float minLength;

	[SerializeField]
	private float progressLength;

	[SerializeField]
	private Text progressText;

	[SerializeField]
	private Text introduction;

	protected virtual void OnDisable()
	{
	}

	protected virtual void Update()
	{
	}

	public void SetProgress(float progress)
	{
	}

	public void SetIntroduction(string text)
	{
	}

	public void Play(float totalTime)
	{
	}

	public void Show(float showTime = 3f)
	{
	}
}
