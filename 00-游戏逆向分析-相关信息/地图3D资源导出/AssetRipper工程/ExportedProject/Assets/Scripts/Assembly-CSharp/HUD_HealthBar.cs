using UnityEngine;
using UnityEngine.UI;

public class HUD_HealthBar : HUD_ProjectionSign
{
	[SerializeField]
	private Text entityName;

	[SerializeField]
	private Image bar;

	private HealthData health;

	protected override void Update()
	{
	}

	protected override void SetGraphVisible(bool visible)
	{
	}

	public void Bind(Entity entity)
	{
	}
}
