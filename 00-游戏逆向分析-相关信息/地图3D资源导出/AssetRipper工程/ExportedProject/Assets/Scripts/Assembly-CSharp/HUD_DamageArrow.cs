using UnityEngine;
using UnityEngine.UI;

public class HUD_DamageArrow : Singleton<HUD_DamageArrow>
{
	private Image image;

	private RectTransform rectTransform;

	private float hideTime;

	private Color imageColor;

	private Vector3 damageOrigin;

	protected override void Awake()
	{
	}

	private void Update()
	{
	}

	private void Start()
	{
	}

	private void DamageEvent(ref DamageEventData eventData)
	{
	}
}
